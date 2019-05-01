#include <string>
#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <algorithm>

void ssort(std::string &s) {
  std::sort(s.begin(), s.end());
}

int main (int argc, char *argv[]) {
  int lg_class = 0;   //keep track of largest class size
  int numClasses = 0;
  int wordCount = 0;  
  std::string class_name;  //key of largest class
  std::string theWord;  //will hold unsorted word
  std::string userWord; 
  std::unordered_map<std::string, std::vector<std::string>> wordMap;   //map of string keys and a value of vectors

  std::ifstream file;
  std::string word;

  if(argc != 2) {
    std::cout << "usage:  ./freq <filename>\n";
    std::cout << "goodbye\n";
    return 1;
  }

  file.open(argv[1], std::ios::in);
  if(!file.is_open()){
    std::cout << "Error: could not open file '" << argv[1] << "'\n";
    std::cout << "goodbye\n";
    return 1;
  }

  std::cout << "reading input file...\n";
  while(file >> word) { 
    theWord = word;  //holds the word string
    ssort(word);  //sorted key string
    if(wordMap.count(word) == 0) {    //if we encounter an empty key count it as a class, push the word, and increase word count
      wordMap[word].push_back(theWord);
      numClasses++;
      wordCount++;
    }
    else {
      wordMap[word].push_back(theWord);
      wordCount++;
      if(lg_class < wordMap[word].size()) {  //keep track of the largest class and its size
        lg_class = wordMap[word].size();
        class_name = word;
      }
    }
  }

  std::cout << "Start entering jumbled words (ctrl-d to terminate) " << std::endl;
  std::cout << ">";
  while(std::getline(std::cin, userWord)) {    
    ssort(userWord);
    if(wordMap.count(userWord) == 0) {
      std::cout << "no anagrams found...try again" << std::endl;
      continue;
    } 
    else {
      std::cout << "English Anagrams Found: " << std::endl;
      for(int i = 0; i < wordMap[userWord].size(); i++) {     //search and print words in user key
        std::cout << wordMap[userWord].at(i) << std::endl;
      }
    }
    std::cout << ">";
  }

  std::cout << "> REPORT: " << std::endl;
  std::cout << "num_words             : " << " " << wordCount << std::endl;
  std::cout << "num_classes           : " << numClasses << std::endl;
  std::cout << "size-of-largest-class : " << lg_class << std::endl;
  std::cout << "largest-class key     : " << class_name << std::endl;
  std::cout << "members of largest class: " << std::endl << std::endl;
  for(int i = 0; i < wordMap[class_name].size(); i++) {
    std::cout << " \'" << wordMap[class_name].at(i) << "\'" << std::endl;
  }
}
