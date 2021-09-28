#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <chrono>
#include <functional>
#include <numeric>

#define one_sec 1000

const std::string textfilename = "data/ru/text.csv";
//const std::string text = "data/ch.csv"
const std::string patternsfilenameprefix = "data/ru/patterns_";


// d is the number of characters in the input alphabet
const int d = 256;
// N is the text length
const int N = 100000000;
// N is the text length
const int M_max = 10000000;
//A prime number
const int q = 4294967295;

int counter = 0;

bool compare_by_symbols(const std::vector<int> &text, const std::vector<int> &pattern, int index){
	for(int j=0; j<pattern.size(); ++j){
		if (text[index + j] != pattern[j])
			return false;
	}
	return true;
}


int RabinKarpSearch( const std::vector<int> &text, const std::vector<int> &pattern)
{
	int M = pattern.size();
	int N = text.size();
	int i, j;
	int p = 0; // hash value for pattern
	int t = 0; // hash value for txt
	int h = 1;
	// The value of h would be "pow(d, M-1)%q"
	for (i = 0; i < M - 1; i++)
		h = (h * d) % q;

	// Calculate the hash value of pattern and first
	// window of text
	for (i = 0; i < M; i++)
	{
		p = (d * p + pattern[i]) % q;
		t = (d * t + text[i]) % q;
	}

	// Slide the pattern over text one by one
	for (i = 0; i <= N - M; i++)
	{

		// Check the hash values of current window of text
		// and pattern. If the hash values match then only
		// check for characters one by one
		if (p == t)
		{
			counter++;
			if (compare_by_symbols(text, pattern, i))
				return i;
				
		}

		// Calculate hash value for next window of text: Remove
		// leading digit, add trailing digit
		if ( i < N-M )
		{
			t = (d * (t - text[i] * h) + text[i+M]) % q;

			// We might get negative value of t, converting it
			// to positive
			if (t < 0)
				t = (t + q);
		}
	}
	return -1;
}

int RabinKarpSearch_sum( const std::vector<int> &text, const std::vector<int> &pattern)
{
	int M = pattern.size();
	int N = text.size();
	int i, j;
	int p = 0; // hash value for pattern
	int t = 0; // hash value for txt

	// Calculate the hash value of pattern and first
	// window of text
	for (i = 0; i < M; i++)
	{
		p = (p + pattern[i]) % q;
		t = (t + text[i]) % q;
	}

	// Slide the pattern over text one by one
	for (i = 0; i <= N - M; i++)
	{

		// Check the hash values of current window of text
		// and pattern. If the hash values match then only
		// check for characters one by one
		if (p == t)
		{
			counter++;
			if (compare_by_symbols(text, pattern, i))
				return i;
				
		}

		// Calculate hash value for next window of text: Remove
		// leading digit, add trailing digit
		if ( i < N-M )
		{
			t = (t - text[i] + text[i+M]) % q;

			// We might get negative value of t, converting it
			// to positive
			if (t < 0)
				t = (t + q);
		}
	}
	return -1;
}


int NaiveSearch(const std::vector<int> &text, const std::vector<int> &pattern){
	int N = text.size();
	int M = pattern.size();
	for(int i=0; i < N - M; ++i){
		if (compare_by_symbols(text, pattern, i))
			return i;
	}
	return -1;
}


int measure_search(const std::vector<int> &text, 
				const std::vector<int> &pattern,
				std::function<int(const std::vector<int>&, const std::vector<int> &)> search
)
{
	using std::chrono::high_resolution_clock;
	using std::chrono::duration_cast;
	using std::chrono::duration;
	using std::chrono::milliseconds;
	int total_time = 0;
	int times = 0;
	int index;
	while (total_time < 1 /* * one_sec*/){
		auto t1 = high_resolution_clock::now();
		index = search(text, pattern);
		
		auto t2 = high_resolution_clock::now();
		auto ms_int = duration_cast<milliseconds>(t2 - t1);
		total_time += ms_int.count();
		// std::cout << total_time << std::endl;
		times++;
	}
	// std::cout << index << " ";
	return total_time / times;
}


int main()
{
	std::vector<int> text(N);
	std::vector<int> pattern(10);
	
	// read textfile
	std::fstream textfile(textfilename, std::fstream::in);
	for(int i=0; i < N; ++i){
		textfile >> text[i];
	}
	textfile.close();
	
	// for each pattern make search
	std::string str;
	
	std::vector<int> pattern_lengths = {10, 100, 1000, 10000, 100000, 10000000};
	std::cout << "M,NaiveSearch_time,RabinKarpSearch_time" << std::endl;
	std::vector<int> NaiveSearch_time;
	std::vector<int> RabinKarp_time;
	for(auto length: pattern_lengths){
		std::fstream pfile(patternsfilenameprefix + std::to_string(length) + ".txt", std::fstream::in);	
		std::cout << length << ",";
		
		NaiveSearch_time.clear();
		RabinKarp_time.clear();
		pattern.resize(length);
			
		while(std::getline(pfile, str)) 
		{
			std::istringstream ss(str);
			int num;
			
			int M = 0;
			while(ss >> num)
			{
				pattern[M] = num;
				M++;
			}
			// for(auto p: pattern)
			//	std::cout << p << " ";
			//std::cout << NaiveSearch(text, pattern) << ",";
			//std::cout << RabinKarpSearch(text, pattern) << ",";
			//std::cout << counter <<",";
			NaiveSearch_time.push_back(measure_search(text, pattern, NaiveSearch));
			RabinKarp_time.push_back(measure_search(text, pattern, RabinKarpSearch));
			//std::cout << measure_search(text, pattern, RabinKarpSearch_sum) << std::endl;
			
			
		}
		std::cout <<  std::accumulate(NaiveSearch_time.begin(), NaiveSearch_time.end(), 0) / 50. << ",";
		std::cout <<  std::accumulate(RabinKarp_time.begin(), RabinKarp_time.end(), 0) / 50. << std::endl;
		
		pfile.close();
	}
	return 0;
}

