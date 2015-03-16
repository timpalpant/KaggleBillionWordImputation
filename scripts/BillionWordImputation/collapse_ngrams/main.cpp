//
//  main.cpp
//  collapse_ngrams
//
//  Reads Google Books ngrams from stdin, summing the total frequency
//  across all years, and outputs just the ngram and total frequency.
//
//  Created by Timothy Palpant on 9/18/14.
//  Copyright (c) 2014 Timothy Palpant. All rights reserved.
//

#include <iostream>
#include <vector>

typedef std::pair<std::string, unsigned long long> yearfreq;
typedef std::vector<yearfreq> yearfreqlist;

void print_ngram(const std::string& ngram, const unsigned long long total_freq,
                 const yearfreqlist& year_freq) {
    std::cout << ngram << '\t' << total_freq;
    for (const yearfreq& yf : year_freq) {
        std::cout << '\t' << yf.first << ',' << yf.second;
    }
    std::cout << std::endl;
}

int main(int argc, const char * argv[]) {
    std::cin.sync_with_stdio(false);
    
    std::string prev_ngram;
    std::string ngram, year, freq, volume;
    yearfreqlist year_freq;
    // Manually read the first line to avoid needing to
    // check for null on every loop iteration.
    std::getline(std::cin, prev_ngram, '\t');
    std::getline(std::cin, year, '\t');
    std::getline(std::cin, freq, '\t');
    unsigned long long ngram_freq = std::stoull(freq);
    unsigned long long total_freq = ngram_freq;
    while (std::getline(std::cin, volume)) {
        std::getline(std::cin, ngram, '\t');
        std::getline(std::cin, year, '\t');
        std::getline(std::cin, freq, '\t');
        ngram_freq = std::stoull(freq);
        if (ngram == prev_ngram) { // same ngram, different year
            total_freq += ngram_freq;
            year_freq.push_back(yearfreq(year, ngram_freq));
        } else { // new ngram, write out previous ngram data
            print_ngram(prev_ngram, total_freq, year_freq);
            prev_ngram = ngram;
            total_freq = ngram_freq;
            year_freq.push_back(yearfreq(year, ngram_freq));
            year_freq.clear();
        }
    }
    
    // Print the final ngram counts
    print_ngram(prev_ngram, total_freq, year_freq);
    
    return 0;
}
