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

#include <boost/algorithm/string.hpp>

#define KENLM_MAX_ORDER 5
#define HAVE_ZLIB 1
#define HAVE_BZLIB 1
#define HAVE_XZLIB 1

#include "lm/config.hh"
#include "lm/model.hh"
#include "lm/enumerate_vocab.hh"

using namespace std;
using namespace lm;
using namespace lm::ngram;

typedef vector<WordIndex> Tokens;

class Dictionary : public EnumerateVocab {
private:
  vector<StringPiece> data_;
public:
  void Add(WordIndex index, const StringPiece& str) {
    data_.push_back(str);
  }
  
  const StringPiece& get(const int i) const {
    return data_[i];
  }
};

struct Guess {
  int location;
  WordIndex word;
  float probability = -1000000;
  
  Guess() : Guess(-1) { }
  
  Guess(const int loc) {
    location = loc;
  }
};

vector<float> score_sentence(const TrieModel& model, const Tokens& words) {
  cerr << "Scoring sentence" << endl;
  State state(model.BeginSentenceState()), out_state;
  vector<float> p;
  for (const WordIndex word : words) {
    p.push_back(model.Score(state, word, out_state));
    state = out_state;
  }
  return p;
}

Guess max_prob_word_at(const Tokens& words, const int i, const TrieModel& model,
                       const vector<float>& p_original) {
  // For a word inserted at position i, we need to rescore
  // the states that include this word, i.e. i-n ... i+n
  Guess best(i);
  Tokens inserted;
  WordIndex offset = max(0, i-int(model.Order())+1);
  State state(model.BeginSentenceState()), out_state;
  for (WordIndex j = offset; j < i; j++) {
    // words before i that i is conditional on
    model.Score(state, words[j], out_state);
    state = out_state;
  }
  inserted.push_back(0); // the inserted word at position i
  for (WordIndex j = i; j < min(int(words.size()),i+model.Order()-1); j++) {
    inserted.push_back(words[j]); // words after i with state that is conditional on i
  }
  
  // now rescore affected words for each candidate insertion from vocab.
  // TODO we could reuse the state more effectively
  const SortedVocabulary& vocab = model.GetVocabulary();
  
  for (WordIndex word = 0; word < vocab.Bound(); word++) {
    inserted[i-offset] = word;
    float p;
    for (const WordIndex word : words) {
      p += model.Score(state, word, out_state);
      state = out_state;
    }
    
    if (p > best.probability) {
      best.probability = p;
      best.word = word;
    }
  }
  
  // compute total probability of words not affected by insert at i
  for (int j = 0; j < i; j++) {
    best.probability += p_original[j]; // words before state that conditions i
  }
  for (int j = i+model.Order(); j < words.size(); j++) {
    best.probability += p_original[j]; // words after state conditioned on i
  }
  
  return best;
}

Guess find_missing_word(const TrieModel& model, const Tokens& words) {
  if (words.size() <= 2) {
    cerr << "Sentence has only " << words.size() << " words" << endl;
    return max_prob_word_at(words, 1, model, p_original);
  }
  
  Guess best, i_best;
  // Missing word cannot be the first or last (see rules)
  for (int i = 1; i < words.size()-1; i++) {
    cerr << "Considering words inserted at " << i << endl;
    i_best = max_prob_word_at(words, i, model, p_original);
    if (i_best.probability > best.probability) {
      best = i_best;
    }
  }
  
  return best;
}

Tokens parse_sentence(const string& s, const SortedVocabulary& vocab) {
  stringstream ss(s);
  std::string item;
  Tokens words;
  while (getline(ss, item, ' ')) {
    words.push_back(vocab.Index(item));
  }
  return words;
}

int main(int argc, const char * argv[]) {
  if (argc < 4) {
    cerr << "USAGE: BillionWordImputation model.kenlm guessed_locations.txt guessed_words.txt" << endl;
    exit(2);
  }
  
  cerr << "Loading KenLM model" << endl;
  Dictionary* dict = new Dictionary();
  Config cfg;
  cfg.enumerate_vocab = dict;
  TrieModel model(argv[1], cfg);
  const SortedVocabulary& vocab = model.GetVocabulary();
  
  cerr << "Processing sentences" << endl;
  ofstream guessed_locations(argv[2]);
  ofstream guessed_words(argv[3]);
  string sentence;
  while (getline(cin, sentence)) {
    Tokens words = parse_sentence(sentence, vocab);
    Guess guess = find_missing_word(model, words);
    guessed_locations << guess.location << endl;
    guessed_words << dict->get(guess.word) << endl;
  }
  
  guessed_locations.close();
  guessed_words.close();
}
