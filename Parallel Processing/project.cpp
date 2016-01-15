#include <iostream>
#include <new>
#include <pthread.h>
#include "timer.h"
#include <stdlib.h>
#include <string>
#include <fstream>
using namespace std;

int ** H;
int ** T;
int match = 1;
int miss = -2;
int gap = -2;
int maxi = 0, maxj = 0;
int length1, length2, thread_count;
int seq;
int lines;
string s1, s2, r1, r2;
pthread_mutex_t mutex1;
pthread_mutex_t ** mutex_array;

int s(const char a,const char b);
int deletion(int i, int j);
int insertion(int i, int j);

void *slave(void *arg);
void slave_serial();
void traceback();

int main(int argc, char *argv[])
{
    
	double begin, end, diff;

	seq = atoi(argv[1]);
	lines = atoi(argv[2]);
	
	ifstream my_file ("chr1.fa");
	string line;
	if (my_file.is_open()){
		int i = 0;
		while (getline(my_file, line) && i < lines){
			s1 = s1 + line;
			i++;
		}
		my_file.close();
	}
	
	ifstream file ("Project-10-seqs.fa");
	if(file.is_open()){
		for(int i=0; i<seq*2;i++)
			getline(file, line);
		s2 = line;
		file.close();
	}


	thread_count = atoi(argv[3]);
	pthread_t myThreads[thread_count];
  	pthread_mutex_init(&mutex1, NULL);
    
	length1 = s1.length();
	length2 = s2.length();

	mutex_array = new pthread_mutex_t * [thread_count - 1];
	for (int i=0; i<length2+1; i++)
		mutex_array[i] = new pthread_mutex_t [length2+1];


	for (int i=0; i<thread_count; i++)
		for (int j=0; j<length2+1; j++){
			pthread_mutex_init(&mutex_array[i][j], NULL);
			pthread_mutex_lock(&mutex_array[i][j]);
		}
	pthread_mutex_unlock(&mutex_array[0][0]);
    
	GET_TIME(begin);
    
	H = new int * [length1+1];
	for(int i=0;i<=length1;i++)
		H[i] = new int [length2+1];
    
	T = new int * [length1+1];
	for(int i=0;i<=length1;i++)
		T[i] = new int [length2+1];
    
	slave_serial();
    
	traceback();
    
	GET_TIME(end);
    
	cout<<endl<<"Serial:"<<endl;
    /*
	for(int i=0;i<=length1;i++){
		for(int j=0;j<=length2;j++)
			cout<<H[i][j]<<" ";
		cout<<endl;
	}
    
	cout<<endl<<"Traceback:"<<endl;
    
	for(int i=0;i<=length1;i++){
		for(int j=0;j<=length2;j++)
			cout<<T[i][j]<<" ";
		cout<<endl;
	}
	*/
	cout<<"r1: "<<r1<<endl;
	cout<<"r2: "<<r2<<endl;
    
	diff = end - begin;
	cout<<"In: "<<diff<<" seconds"<<endl;
    
    
	for(int i=0;i<length1;i++)
    	delete [] H[i];
  	delete [] H;
    
  	for(int i=0;i<length1;i++)
    	delete [] T[i];
  	delete [] T;
    
  	r1 = "";
  	r2 = "";
    
    maxi = 0;
    maxj = 0;
    
  	GET_TIME(begin);
    
	H = new int * [length1+1];
	for(int i=0;i<=length1;i++)
		H[i] = new int [length2+1];
    
	T = new int * [length1+1];
	for(int i=0;i<=length1;i++)
		T[i] = new int [length2+1];

		for(long j=0; j<thread_count;j++)
			pthread_create(&myThreads[j], NULL, slave, (void *) j);
        
		for(int j=0; j<thread_count;j++)
			pthread_join(myThreads[j], NULL);
    
	traceback();
    
	GET_TIME(end);
    
	cout<<endl<<"Parallel:"<<endl;
    /*
	for(int i=0;i<=length1;i++){
		for(int j=0;j<=length2;j++)
			cout<<H[i][j]<<" ";
		cout<<endl;
	}
    
	cout<<endl<<"Traceback:"<<endl;
    
	for(int i=0;i<=length1;i++){
		for(int j=0;j<=length2;j++)
			cout<<T[i][j]<<" ";
		cout<<endl;
	}
	*/
	cout<<"r1: "<<r1<<endl;
	cout<<"r2: "<<r2<<endl;
    
	diff = end - begin;
	cout<<"In: "<<diff<<" seconds"<<endl;
    
    
	for(int i=0;i<length1;i++)
    	delete [] H[i];
  	delete [] H;
    
  	for(int i=0;i<length1;i++)
    	delete [] T[i];
  	delete [] T;
    
	return 0;
}

void slave_serial ()
{
	for(int i=0;i<=length2;i++)
		H[0][i] = 0;
	for(int i=0;i<length1;i++)
		H[i][0] = 0;
    
	for(int i=0;i<=length2;i++)
		T[0][i] = 0;
	for(int i=0;i<length1;i++)
		T[i][0] = 0;
    
	for(int i=1;i<=length1;i++){
		for(int j=1;j<=length2;j++){
			H[i][j] = max(
                          max(H[i-1][j-1]+s(s1.at(i-1),s2.at(j-1)),0),
                          max(H[i-1][j]+gap,H[i][j-1]+gap)
                          );
			if (H[i][j] == 0)
				T[i][j] = 0;
			else if (H[i][j] == H[i-1][j-1]+s(s1.at(i-1),s2.at(j-1)))
				T[i][j] = 1;
			else if (H[i][j] == H[i-1][j]+gap)
				T[i][j] = 2;
			else T[i][j] = 3;
            
			if(H[i][j] > H[maxi][maxj]){
				maxi = i;
				maxj = j;
			}
		}
	}
}

void *slave(void *arg)
{
	long id = (long) arg;

	int start_index, end_index;
    
    if(id < (length1+1)%thread_count){
    	start_index = id * ((length1+1)/thread_count) + id;
    	end_index = start_index + ((length1+1)/thread_count);
    }
  	else {
  		start_index = id * ((length1+1)/thread_count) + ((length1+1)%thread_count);
  		end_index = start_index + ((length1+1)/thread_count) - 1;
  	}

  	int locali = id;
	int localj = start_index;

	if(id == 0){
		for (int j=0; j<length2+1; j++){

			for(int i=start_index; i <= end_index; i++){
		        if (i == 0 || j == 0)
		            H[i][j] = 0;
		        else H[i][j] = max(
		                           max(H[i-1][j-1]+s(s1.at(i-1),s2.at(j-1)),0),
		                           max(H[i-1][j]+gap,H[i][j-1]+gap)
		                           );
		        if (H[i][j] == 0)
		            T[i][j] = 0;
		        else if (H[i][j] == H[i-1][j-1]+s(s1.at(i-1),s2.at(j-1)))
		            T[i][j] = 1;
		        else if (H[i][j] == H[i-1][j]+gap)
		            T[i][j] = 2;
		        else T[i][j] = 3;
		        
		        if(H[i][j] >= H[locali][localj]){
		            locali = i;
		            localj = j;
		        }
			}

			pthread_mutex_unlock(&mutex_array[id][j]);
		}
    }

    else {
    	for (int j=0; j<length2+1; j++){
    		pthread_mutex_lock(&mutex_array[id-1][j]);
			for(int i=start_index; i <= end_index; i++){
		        if (i == 0 || j == 0)
		            H[i][j] = 0;
		        else H[i][j] = max(
		                           max(H[i-1][j-1]+s(s1.at(i-1),s2.at(j-1)),0),
		                           max(H[i-1][j]+gap,H[i][j-1]+gap)
		                           );
		        if (H[i][j] == 0)
		            T[i][j] = 0;
		        else if (H[i][j] == H[i-1][j-1]+s(s1.at(i-1),s2.at(j-1)))
		            T[i][j] = 1;
		        else if (H[i][j] == H[i-1][j]+gap)
		            T[i][j] = 2;
		        else T[i][j] = 3;
		        
		        if(H[i][j] >= H[locali][localj]){
		            locali = i;
		            localj = j;
		        }
			}

			pthread_mutex_unlock(&mutex_array[id][j]);
		}
    }
   	pthread_mutex_lock(&mutex1);
	if(H[locali][localj] > H[maxi][maxj]){
		maxi = locali;
		maxj = localj;
	}
	pthread_mutex_unlock(&mutex1);
    
	return NULL;
}

int s(const char a, const char b)
{
	if(a == b)
		return match;
    
	return miss;
}

void traceback()
{
	int i=maxi, j=maxj;
    
	while(T[i][j] != 0){
		if(T[i][j] == 1){
			r1 = s1.at(i-1) + r1;
			r2 = s2.at(j-1) + r2;
			j--;
			i--;
		}
		else if (T[i][j] == 2){
			r1 = s1.at(i-1) + r1;
			r2 = "-" + r2;
			i--;
		}
		else {
			r1 = "-" + r1;
			r2 = s2.at(j-1) + r2;
			j--;
		}
	}
    
}