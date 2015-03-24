//
//  main.cpp
//  BillionWordImputation
//
//  Created by Timothy Palpant on 9/18/14.
//  Copyright (c) 2014 Timothy Palpant. All rights reserved.
//

#include <iostream>
#include <string>
#include <fstream>
#include <list>

#define KENLM_MAX_ORDER 6
#define HAVE_ZLIB 1
#define HAVE_BZLIB 1
#define HAVE_XZLIB 1
#define KEEP_TOP_N 5
#define MAX_VOCAB_SIZE 50000

#include "lm/config.hh"
#include "lm/model.hh"
#include "lm/enumerate_vocab.hh"
#include "lm/binary_format.hh"
#include "lm/model_type.hh"

using namespace std;
using namespace lm;
using namespace lm::ngram;

typedef vector<WordIndex> Tokens;

template <typename T>
T logsumexp(const vector<T>& nums) {
  T max_exp = *max_element(nums.cbegin(), nums.cend());
  T sum = 0.0;
  for (const T x : nums)
    sum += pow(10.0, x - max_exp);
  return log10(sum) + max_exp;
}

class Dictionary : public EnumerateVocab {
private:
  vector<string> data_;
public:
  void Add(WordIndex index, const StringPiece& str) {
    data_.push_back(str.as_string());
  }
  
  const string& get(const int i) const {
    return data_[i];
  }
  
  size_t size() const {
    return data_.size();
  }
};

vector<size_t> merge_locations(const vector<float>& p_anywhere,
                               const size_t location,
                               const vector<float>& p_at_location,
                               const vector<size_t>& other_locations) {
  size_t i = 0, j = 0;
  vector<size_t> merged(other_locations.size());
  for (size_t k = 0; k < merged.size(); k++) {
    if (p_anywhere[i] > p_at_location[j]) {
      merged[k] = other_locations[i];
      i++;
    } else {
      merged[k] = location;
      j++;
    }
  }
  
  return merged;
}

class Guess {
public:
  size_t location;
  WordIndex word;
  vector<float> p_at_location; // P(sentence) for best N words at this location
  vector<float> p_surrounding; // P(word | context) for N-grams including word
  vector<float> p_at_other_location; // P(sentence) for best N words at a different location
  vector<float> p_anywhere; // P(sentence) for the best N words at any location
  vector<float> Z; // sum P(sentence) for each insertion location
  float Z_location; // sum P(sentence) for best insertion location
  vector<size_t> other_locations; // location corresponding to each entry in p_anywhere
  
  Guess() : Guess(-1) { }
  
  Guess(const int loc) : p_at_location(KEEP_TOP_N, -numeric_limits<float>::infinity()),
                         p_anywhere(KEEP_TOP_N, -numeric_limits<float>::infinity()),
                         other_locations(KEEP_TOP_N, -1) {
    location = loc;
    Z.reserve(MAX_VOCAB_SIZE);
  }
  
  void update(const WordIndex word, const float p, const vector<float>& p_surrounding) {
    if (p > p_at_location.back()) { // new word in top N
      // find rank of new word
      auto insert = lower_bound(p_at_location.crbegin(), p_at_location.crend(), p);
      size_t i = p_at_location.size() - distance(p_at_location.crbegin(), insert);
      
      // shift worse words down by one
      for (size_t j = p_at_location.size()-1; j > i; j--) {
        p_at_location[j] = p_at_location[j-1];
      }
      p_at_location[i] = p;
      
      if (i == 0) { // new best word
        this->word = word;
        this->p_surrounding = p_surrounding;
      }
    }
    
    Z.push_back(p);
  }
  
  void update(const Guess& other) {
    Z.push_back(logsumexp(other.Z));
    
    if (other.p_at_location.front() > p_anywhere.back()) {
      vector<float> merged(p_anywhere.size()+other.p_at_location.size());
      merge(p_anywhere.crbegin(), p_anywhere.crend(),
            other.p_at_location.crbegin(), other.p_at_location.crend(),
            merged.rbegin());
      merged.resize(KEEP_TOP_N);
      other_locations = merge_locations(p_anywhere, other.location, other.p_at_location, other_locations);
      p_anywhere = merged;
    }
    
    if (other.p_at_location.front() > p_at_location.front()) { // new best
      location = other.location;
      word = other.word;
      p_at_other_location = p_at_location;
      p_at_location = other.p_at_location;
      p_surrounding = other.p_surrounding;
      Z_location = Z.back();
    }
  }
  
  void print_to(ostream& o, const Dictionary* dict) {
    o << location;
    o << '\t' << dict->get(word);
    o << '\t' << logsumexp(Z);
    o << '\t' << Z_location;
    for (const size_t i : other_locations) {
      o << '\t' << (int(i)-int(location));
    }
    for (const float p : p_anywhere) {
      o << '\t' << p;
    }
    for (const float p : p_at_location) {
      o << '\t' << p;
    }
    for (const float p : p_at_other_location) {
      o << '\t' << p;
    }
    for (const float p : p_surrounding) {
      o << '\t' << p;
    }
    o << endl;
  }
};

// fully score list of tokens, populating list of states and probabilities
template <class Model>
void score_sentence(const Model& model, const Tokens& words,
                    vector<State>& states, vector<float>& p) {
  State state(model.BeginSentenceState()), out_state;
  states.reserve(words.size()+1);
  p.reserve(words.size());
  states.push_back(state);
  for (const WordIndex word : words) {
    p.push_back(model.Score(state, word, out_state));
    states.push_back(out_state);
    state = out_state;
  }
}

// find best guess for missing word inserted at location i
template <class Model>
Guess max_prob_word_at(const Model& model, const Tokens& words, const int i,
                       const vector<State>& states, const vector<float>& p) {
  // total probability of words before inserted word
  // or after the n-grams that include the inserted word
  float p_else = 0;
  for (int j = 0; j < i; j++) {
    p_else += p[j];
  }
  for (int j = i+model.Order(); j < p.size(); j++) {
    p_else += p[j];
  }
  
  // Test each word at location i
  // For a word inserted at position i, we need to rescore
  // the states that include this word, i.e. i ... i+n
  Guess best(i);
  State state, out_state;
  const typename Model::Vocabulary& vocab = model.GetVocabulary();
  size_t stop = min(size_t(model.Order()), words.size()-i);
  float p_total, p_w;
  vector<float> p_surrounding(model.Order()+1);
  for (WordIndex word = 0; word < vocab.Bound(); word++) {
    p_total = p_else;
    // score the inserted word at location i
    state = states[i];
    p_w = model.Score(state, word, out_state);
    p_surrounding[0] = p_w;
    p_total += p_w;
    state = out_state;
    // score the N subsequent words whose context depends on i
    for (int j = 0; j < stop; j++) {
      p_w = model.Score(state, words[i+j], out_state);
      p_surrounding[j+1] = p_w;
      p_total += p_w;
      state = out_state;
    }
    
    best.update(word, p_total, p_surrounding);
  }
  
  return best;
}

// find the best guess for a missing word in list of tokens
template <class Model>
Guess find_missing_word(const Model& model, const Tokens& words) {
  vector<State> states;
  vector<float> p;
  score_sentence(model, words, states, p);
  
  if (words.size() <= 1) {
    return max_prob_word_at(model, words, 0, states, p);
  } else if (words.size() <= 2) {
    return max_prob_word_at(model, words, 1, states, p);
  }
  
  Guess best, i_best;
  // Missing word cannot be the first or last (see rules)
  for (int i = 1; i < words.size()-1; i++) {
    i_best = max_prob_word_at(model, words, i, states, p);
    best.update(i_best);
  }
  
  return best;
}

// Given a sentence s, split tokens and lookup vocab ids
template <class Model>
Tokens parse_sentence(const Model& model, const string& s) {
  stringstream ss(s);
  string item;
  Tokens words;
  const typename Model::Vocabulary& vocab = model.GetVocabulary();
  while (getline(ss, item, ' ')) {
    words.push_back(vocab.Index(item));
  }
  return words;
}

template <class Model>
void process_sentences(const Model& model, const Dictionary* dict) {
  cerr << "Model state size = " << size_t(model.Order()) << endl;
  cerr << "Dictionary contains " << dict->size() << " words" << endl;
  
  cerr << "Processing sentences" << endl;
  string sentence;
  unsigned long line_num = 0;
  while (getline(cin, sentence)) {
    Tokens words = parse_sentence(model, sentence);
    Guess guess = find_missing_word(model, words);
    guess.print_to(cout, dict);
    
    if (++line_num % 1000 == 0) {
      cerr << line_num << endl;
    }
  }
}

int main(int argc, const char* argv[]) {
  if (argc < 2) {
    cerr << "USAGE: BillionWordImputation model.kenlm" << endl;
    exit(2);
  }
  
  const char* model_filename = argv[1];
  cerr << "Loading KenLM model: " << model_filename << endl;
  Dictionary* dict = new Dictionary();
  Config cfg;
  cfg.enumerate_vocab = dict;
  ModelType model_type;
  RecognizeBinary(model_filename, model_type);
  switch (model_type) {
    {
    case ModelType::PROBING:
      ProbingModel pmodel(model_filename, cfg);
      process_sentences(pmodel, dict);
      break;
    } {
    case ModelType::TRIE:
      TrieModel tmodel(model_filename, cfg);
      process_sentences(tmodel, dict);
      break;
    } {
    default:
      cerr << "Unsupported model type: " << model_type << endl;
      exit(2);
    }
  }
  
}