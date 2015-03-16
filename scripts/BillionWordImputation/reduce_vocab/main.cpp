//
//  main.cpp
//  reduce_vocab
//
//  Created by Timothy Palpant on 9/19/14.
//  Copyright (c) 2014 Timothy Palpant. All rights reserved.
//

#include <iostream>
#include <unordered_map>

typedef std::unordered_map<std::string, unsigned long long> dict;

dict load_vocab(const std::string& vocab_file) {
  vocab = dict();
  return vocab;
}

int main(int argc, const char * argv[]) {
  std::cin.sync_with_stdio(false);
  
  dict vocab = load_vocab(argv[1]);
  
  std::string token;
  std::unordered_map<std::string, unsigned long long> counts;
  int word_num = 0;
  while (std::cin >> token) {
    if (!counts.count(token)) {
      counts[token] = 1;
    } else {
      counts[token] += 1;
    }
    
    word_num += 1;
    if (word_num % 10000000 == 0) {
      std::cerr << word_num << std::endl;
    }
  }
  
  for (const auto& kv : counts) {
    std::cout << kv.first << '\t' << kv.second << std::endl;
  }
  
  return 0;
}
