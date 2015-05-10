// C++ equivalent for exon_ChIP_extract_from_TagAlign.py
//
// Takes a config file with only one window parameter which is the number of 
// base pairs before and after the locations that will be counted.

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include <iostream>
#include <fstream>
#include <string>
#include <tuple>
#include <vector>
#include <deque>

#define RECENT_LINES_BUFFER_LENGTH 5000

using namespace rapidjson;
using namespace std;

// parse input line
// lines of tagAlign file are 6 tab-separated fields.
//      We are about the first and second, which are the chromosome 
//      and offest
//  On success return 1, if end of file or error, return 0 
int get_read_loc(tuple<int,int>&loc, ifstream & ChIP_file, Document & chr_order){
    string throw_away; // string to hold un-used values at end of lines
    string ChIP_chr_str;
    string ChIP_loc_str;
    getline(ChIP_file,ChIP_chr_str,'\t');
    getline(ChIP_file,ChIP_loc_str,'\t');
    if (! getline(ChIP_file,throw_away)){
        cerr << "getline return 0 when reading ChIP_file" << endl; 
        return 0;
    }

    // read in the site position and interpret it as a decimal integer.
    int ChIP_chr=chr_order[ChIP_chr_str.c_str()].GetInt();
    int ChIP_loc=stoi(ChIP_loc_str);
    loc=tuple <int,int>(ChIP_chr,ChIP_loc);
    // loc=tuple <int,int>(0,0);
    return 1;
}

void reverse(vector <int> & vec){
    vector<int> tmp(vec.size());
    for (int x =vec.size()-1; x >= 0;--x){
        tmp[x]= vec[vec.size()-x-1];
    }  
    vec=tmp;
}

int main(int argc, char** argv) {

    if (argc != 6){
        cerr << "invalid usage: ./chip_extract <config.json>  <sample_ID> <Mark_ID> <sites.json> <chipreads.TagAlign>" <<endl;
        exit(1);
    }


    char *config_fn=argv[1];
    char *sampleID=argv[2];
    char *MarkID=argv[3];
    char *sites_fn=argv[4];
    char *ChIP_fn=argv[5];



    // Open and parse config file 
    ifstream config_file;
    config_file.open(config_fn);
    if (!config_file.is_open()){
        cerr << "could not open config file <" << config_fn << ">" << endl;
        exit(1);
    }

    // Read config file and parse into JSON format
    string config_line;
    getline(config_file,config_line);
    Document config;
    config.Parse(config_line.c_str());
    config_file.close();

    string chr_order_fn = config["chromosome_order_fn"].GetString();
    int window_size = config["window_size"].GetInt();
    // The number of windows of window_size base pairs before and after the 
    // locations provided around which reads are counted
    int num_windows = config["num_windows_per_side"].GetInt();

    // Open and parse chromosome order file
    ifstream chr_file;
    chr_file.open(chr_order_fn);
    if (!chr_file.is_open()){
        cerr << "could not open chromosome order file <"<< chr_order_fn <<">" << endl;
        exit(1);
    }

    string chr_line;
    getline(chr_file,chr_line);
    Document chr_order;
    chr_order.Parse(chr_line.c_str());
    chr_file.close();



    // open file of ordered site locations
    int buff_size=100000;
    ifstream sites_file;
    // char *sites_buff = new char[buff_size];
    char sites_buff [buff_size];
    sites_file.rdbuf()->pubsetbuf(sites_buff,buff_size);
    sites_file.open(sites_fn);
    if (!sites_file.is_open()){
        cerr << "could not open file with sites to label <"<< sites_fn <<">" << endl;
        exit(1);
    }

    string site_line;
    getline(sites_file,site_line);
    Document current_site;
    current_site.Parse(site_line.c_str());
    string site_chr=current_site["seqname"].GetString();
    // read in the site position and interpret it as a decimal integer.
    //int site_pos=stoi(current_site["five_p_loc"].GetString()); 
    int site_pos=current_site["location"].GetInt(); 

    int site_chr_val = chr_order[site_chr.c_str()].GetInt();

    tuple<int,int> site_strt(site_chr_val,site_pos-window_size*num_windows);
    tuple<int,int> site_end(site_chr_val,site_pos+window_size*num_windows);

    // create a vector to hold the read counts for every window that is twice 
    // 'num_windows' because it must hold reads on both sides of the site.
    vector<int> site_reads(num_windows*2);
    for (int x= 0; x < site_reads.size();++x) site_reads[x]=0; // zero it out

    // open up the TagAlign file
    ifstream tag_align_file;
//    char *buff = new char[buff_size];
    char buff [buff_size];
    tag_align_file.rdbuf()->pubsetbuf(buff,buff_size);

    tag_align_file.open(ChIP_fn);
    if (!tag_align_file.is_open()){
        cerr << "could not open tagAlign file <"<< ChIP_fn <<">" << endl;
        exit(1);
    }

    int count=0;
    tuple<int,int> ChIP_read_loc(0,0);
    string throw_away; // string to dump ends of lines that are unused into
    do{
        // print every million or so lines.
        if (!(++count % (1<< 20)) ) cerr << "line: " << count <<" \n";
        if (!get_read_loc(ChIP_read_loc,tag_align_file,chr_order)){
            cerr << "get_read_loc returned 0, exitting now" << endl;
            exit(0);
        }
        // if the the read is before the current site, continue to the next read 
        if (ChIP_read_loc < site_strt) continue;

        // if the read is with the range of the current site add it to the count.
        if (ChIP_read_loc <= site_end) {
            int bin_idx = int((get<1>(ChIP_read_loc)-get<1>(site_strt))/window_size);
            if( bin_idx == 2*num_windows) --bin_idx;
            site_reads[bin_idx]+=1;
            continue;
        }

        //at this point we know the read is past the current site, so we must move to the next site.
        if (current_site["strand"].GetInt() == -1){
            reverse(site_reads);
        }

        cout << site_chr << string("\t") << site_pos << string("\t") << sampleID << string("\t") << MarkID << "\t[" ;
        for (int x= 0; x < site_reads.size()-1;++x) 
            cout << site_reads[x] << string(", ");
        cout <<site_reads[site_reads.size()-1];
        cout << string("]") ;
        cout << endl;
//        cout<< "#" << current_site["five_p_loc"].GetString() << endl;
/*
           Value &sample_dict = current_site[sample_ID];
           string sample_json= sample_dict.GetString();
           Document new_sample_doc;
           new_sample_doc.Parse(sample_json);
           Value myArray(kArrayType);
           myArray.SetObject();
           Document::AllocatorType& allocator = new_sample_doc.GetAllocator();
           for ( int i = 0; i < site_reads.size();++i){
           myArray.PushBack(site_reads[i],allocator);
           } 
*/

        // trace back in case windows are overlapping
        int dist_to_go_back = int(tag_align_file.tellg())>10000? 10000:int( tag_align_file.tellg()); 
        tag_align_file.seekg(-dist_to_go_back,tag_align_file.cur);
        if (!getline(tag_align_file,throw_away)){
            cerr << "error after seeking back in tag align file" <<endl;
            exit(1);
        }

        // first print out the current site with the new read count info
        if (!getline(sites_file,site_line)) break;
        current_site.Parse(site_line.c_str()); 

        // reset site_reads
        for (int x= 0; x < site_reads.size();++x) site_reads[x]=0; // zero it out

        site_chr=current_site["seqname"].GetString();
        site_pos=current_site["location"].GetInt(); 
        //site_pos=stoi(current_site["five_p_loc"].GetString()); 

        site_chr_val = chr_order[site_chr.c_str()].GetInt();
        site_strt=tuple<int,int>(site_chr_val,site_pos-window_size*num_windows);
        site_end=tuple<int,int> (site_chr_val,site_pos+window_size*num_windows);

    }while (true);

    sites_file.close();
    tag_align_file.close();

    return 0;
}
