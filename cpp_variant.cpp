#include <iostream>
#include <fstream>
#include <array>
#include <vector>
#include <algorithm>
#include <cmath> 
#include <string>
#include <random>


typedef unsigned long long int ullong; 
using std::vector;


const vector<double> pr = {90, 30, 30, 14, 6};
double alpha = 0.05;
unsigned long long int max_iter = 1e+8;
int nResults = pr.size();
int s = nResults; // ????????????


void report(vector<double> &f_sol, vector<ullong> &counter, ullong nIter);


double delta(ullong n, int s){
    return std::sqrt((2. / static_cast<double>(n)) * std::log(s / alpha));
}

int main(){
	std::random_device rd;
    std::mt19937 g(rd());
	std::discrete_distribution<> gen(pr.begin(), pr.end());
	ullong n = 0;
	vector<double> f_sol(s);
	vector<ullong> counter(nResults);
	bool cont = true;
	while (cont){
		++n;
		int exp_result = gen(g);
		++counter[exp_result];
		double sum = 0.;
		double freq_curr = counter[0] / n;
		cont = false; 
		for (int i = 0; i < f_sol.size(); ++i)
		{	
			freq_curr = static_cast<double>(counter[i]) / static_cast<double>(n);
			sum += freq_curr;
			f_sol[i] = sum + freq_curr;
			if (fabs(f_sol[i] - 1) <= delta(n, s)) 
				cont = true;
		}
		if (n % 100000000 == 0)
		{
			//break;
			std::cout<< n << std::endl;
		}
	}
	
	report(f_sol, counter, n);
	

 	//std::cin.get();
	return 0;
}


void report(vector<double> &f_sol, vector<ullong> &counter, ullong nIter)
{
	std::cout.precision(3);
	std::cout.setf( std::ios::fixed, std:: ios::floatfield );
	
	std::cout << "probabilities :" << std::endl; 
	std::cout << "pr1\t"; 
	double total = std::accumulate(pr.begin(), pr.end(), 0);
	for (int i = 1; i < pr.size(); ++i){
		std::string symbol = (pr[i - 1] > pr[i]) ? ">" : "=";
		std::cout << symbol << "\t" << "pr" << std::to_string(i + 1) << "\t";
	}
	std::cout << std::endl;
	std::cout << pr[0] / total << "\t"; 
	for (int i = 1; i < pr.size(); ++i){
		std::string symbol = (pr[i - 1] > pr[i]) ? ">" : "=";
		std::cout << symbol << "\t" << pr[i] / total << "\t";
	}
	std::cout << std::endl<< std::endl;
	
	std::cout << nIter <<" iterations" << std::endl;
	std::cout << std::endl;
	
	std::cout << "Frequencies :" << std::endl; 
	for (int i = 0; i < counter.size(); ++i)
		std::cout << "nu" << std::to_string(i + 1) << "\t|\t"; 
	std::cout << std::endl;
	for (auto c: counter)
		std::cout << c / static_cast<double>(nIter) << "\t|\t"; 
	std::cout << std::endl << std::endl;
	
	std::cout << "Possibilities: " << std::endl;
	std::cout << "1 = p1"; 
	for (int i = 0; i < f_sol.size(); ++i){
		std::string symbol = (f_sol[i] > 1) ? ">" : "=";
		std::cout << "\t" << symbol << "\t" << "p" << std::to_string(i + 2) ;
	}
	std::cout << " = 0" << std::endl;
	
	std::cout << "0."; 
	for (int i = 0; i < f_sol.size(); ++i){
		std::string symbol = (f_sol[i] > 1) ? "1" : "0";
		std::cout << symbol;
	}
	return;
}




