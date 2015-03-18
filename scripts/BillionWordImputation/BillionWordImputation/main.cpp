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

#define KENLM_MAX_ORDER 6
#define HAVE_ZLIB 1
#define HAVE_BZLIB 1
#define HAVE_XZLIB 1

#include "lm/config.hh"
#include "lm/model.hh"
#include "lm/enumerate_vocab.hh"
#include "lm/binary_format.hh"
#include "lm/model_type.hh"

using namespace std;
using namespace lm;
using namespace lm::ngram;

typedef vector<WordIndex> Tokens;

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

struct Guess {
  int location;
  WordIndex word;
  float probability = -1000000;
  float second_best = -1000000;
  float best_at_different_location = -1000000;
  
  Guess() : Guess(-1) { }
  
  Guess(const int loc) {
    location = loc;
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
  float p_total;
  for (WordIndex word = 0; word < vocab.Bound(); word++) {
    p_total = p_else;
    // score the inserted word at location i
    state = states[i];
    p_total += model.Score(state, word, out_state);
    state = out_state;
    // score the N subsequent words whose context depends on i
    for (int j = 0; j < stop; j++) {
      p_total += model.Score(state, words[i+j], out_state);
      state = out_state;
    }
    
    if (p_total > best.probability) {
      best.word = word;
      best.second_best = best.probability;
      best.probability = p_total;
    }
  }
  
  return best;
}

// find the best guess for a missing word in list of tokens
template <class Model>
Guess find_missing_word(const Model& model, const Tokens& words) {
  vector<State> states;
  vector<float> p;
  score_sentence(model, words, states, p);
  
  if (words.size() == 0) {
    return max_prob_word_at(model, words, 0, states, p);
  } else if (words.size() <= 2) {
    return max_prob_word_at(model, words, 1, states, p);
  }
  
  Guess best, i_best;
  // Missing word cannot be the first or last (see rules)
  for (int i = 1; i < words.size()-1; i++) {
    i_best = max_prob_word_at(model, words, i, states, p);
    if (i_best.probability > best.probability) { // new best
      if (best.probability > i_best.second_best) {
        // previous best is better than any other word inserted at i
        i_best.second_best = best.probability;
      } // else second best word at i is better than all previous
      
      // previous best was at a different location
      i_best.best_at_different_location = best.probability;
      best = i_best;
    }
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
    float location_odds = guess.probability - guess.best_at_different_location;
    float word_odds = guess.probability - guess.second_best;
    cout << guess.location << '\t' << location_odds
    << '\t' << dict->get(guess.word) << '\t' << word_odds << endl;
    
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