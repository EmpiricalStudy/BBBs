# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 23:49:22 2023

@author: hren_
"""


import datetime
import os
from bs4 import BeautifulSoup
import csv
import json
import re
#import nltk
#from nltk.stem.porter import PorterStemmer 
#from nltk.corpus import stopwords
import string
from datetime import datetime
import pandas as pd
import codecs
import random
from sklearn.metrics import cohen_kappa_score


def get_root_path(repo):
    pre_repos=['eclipse','freedesktop','mozilla','netbeans','openoffice']
    new_repos=['Gentoo','GNOME','KDE','LinuxKernel']
    pre_root_path='F:/network/'
    new_root_path='D:/breakable-blocking-bugs/'
    
    if(repo in pre_repos):
        return pre_root_path
    if(repo in new_repos):
        return new_root_path

def get_blocking_bugs(repos):
    
    for repo in repos:
        
        file=open('../{}/{}_blocking_bugs.csv'.format(repo,repo),'w',encoding='utf8',newline='')
        f=open('../{}/blocked_bugs.txt'.format(repo),'w',encoding='utf8')
        header=['down_bug','up_bug']
        file_csv=csv.DictWriter(file,header)
        file_csv.writeheader()
        
        bugs=[]
        blocking_bugs=[]
        blocked_bugs=[]
        blocking_bug_pairs=[]
        for root,dirs,files in os.walk('../{}/data/'.format(repo)):
            
            for file in files:
                
                bug=file.split('.')[0][1:]
                bugs.append(bug)
                
                temp_path=os.path.join(root,file)
                #print(temp_path)
                soup = BeautifulSoup(open(temp_path,encoding='utf8'),"xml")
                #print(soup.prettify())
                
                print(repo,bug)
                for block in soup.find_all("blocked"):
                    print('has blocking .......')
                    blocking_bugs.append(bug)
                    blocking_bug_pairs.append(bug+'#'+block.string)
                    blocked_bugs.append(block.string)
                    
                    #print(bug,block)
                    #print(file,block.string)
                for block in soup.find_all("dependson"):
                    blocked_bugs.append(bug)
                    blocking_bug_pairs.append(block.string+'#'+bug)
                    blocking_bugs.append(block.string)
                    
            for blocked in set(blocked_bugs):
                f.write(blocked+'\t\n')
            for bug_pair in set(blocking_bug_pairs):
                file_csv.writerow({'down_bug':bug_pair.split('#')[1],'up_bug':bug_pair.split('#')[0]})

def get_fix_time(path,repo):
    fix_time=''
    soup=BeautifulSoup(open(path,encoding='utf8').read(),'html.parser')
    if(not soup.table):
        return fix_time
    if(repo=='netbeans'):
        if(not soup.table.table):
            return fix_time
        table=soup.table.table
    elif(repo=='openoffice' or repo=='GNOME'):
        tables=soup.find_all('table')
        table=tables[-1]
    else:
        table=soup.table
    trs=table.find_all('tr')  
    for i in range(1,len(trs)):
        tds=trs[i].find_all("td")
        
        if(len(tds)==5):
            #people=tds[0].get_text()
            time=tds[1].get_text()
            if(tds[4].get_text().strip()=='FIXED'):
                fix_time=time  
        else:
            if(tds[2].get_text().strip()=='FIXED'):
                fix_time=time
    return(fix_time)
    

def get_breakable_blocking_bugs(repos):
    for repo in repos:
        files=os.listdir('../{}/data/'.format(repo))
        total_bugs=[]
        for file in files:
            total_bugs.append(file.split('.')[0][1:])
        
        all_bugs=[]
        for file in os.listdir('../{}/new_activity/'.format(repo)):
            all_bugs.append(file.split('.')[0][1:])
            
        blocking_bugs=[]
        total_blocking_bugs=[]
        b_blocking_bugs=[]
        
        blocked_bugs=[]
        total_blocked_bugs=[]
        b_blocked_bugs=[]
        
        total_bug_pairs=[]
        blocking_bug_pairs=[]
        b_blocking_bug_pairs=[]
        
        with open('../{}/{}_blocking_bugs.csv'.format(repo,repo),'r',encoding='utf8') as file:
            reader=csv.DictReader(file)
            for row in reader:
                total_blocking_bugs.append(row['up_bug'])
                total_blocked_bugs.append(row['down_bug'])
                bb_bug=row['up_bug']
                bed_bug=row['down_bug']
                total_bug_pairs.append((bb_bug,bed_bug))
                if(bed_bug not in all_bugs):
                    print('do not have activity information.......')
                    continue
                
                bb_time=get_fix_time('../{}/new_activity/a{}.htm'.format(repo,bb_bug),repo)
                bed_time=get_fix_time('../{}/new_activity/a{}.htm'.format(repo,bed_bug),repo)
                
                if(bb_time=='' or bed_time==''):
                    continue
                
                bb_fix_time=' '.join(bb_time.split(' ')[:2])
                bed_fix_time=' '.join(bed_time.split(' ')[:2])
                
                bb_fix_time = datetime.datetime.strptime(bb_fix_time, '%Y-%m-%d %H:%M:%S')
                bed_fix_time = datetime.datetime.strptime(bed_fix_time, '%Y-%m-%d %H:%M:%S')
                
                if(bed_fix_time<bb_fix_time):
                    
                    b_blocking_bugs.append(bb_bug)
                    b_blocked_bugs.append(bed_bug)
                    b_blocking_bug_pairs.append((bb_bug,bed_bug))
                else:
                    blocking_bugs.append(bb_bug)
                    blocked_bugs.append(bed_bug)
                    blocking_bug_pairs.append((bb_bug,bed_bug))
            file.close()
        
        print(len(total_bugs),len(set(total_blocking_bugs)),len(total_blocking_bugs),len(set(blocking_bugs)),len(total_bug_pairs),len(b_blocking_bug_pairs),len(b_blocking_bugs),len(set(b_blocking_bugs)))
        
        with open('../{}/total_bugs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(total_bugs,file)
            file.close()
        with open('../{}/total_blocking_bugs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(list(set(total_blocking_bugs)),file)
            file.close()
        with open('../{}/blocking_bugs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(list(set(blocking_bugs)),file)
            file.close()
        with open('../{}/breakable_blocking_bugs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(list(set(b_blocking_bugs)),file)
            file.close()
        with open('../{}/breakable_blocking_bug_pairs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(list(b_blocking_bug_pairs),file)
            file.close()
        with open('../{}/total_blocking_bug_pairs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(list(total_bug_pairs),file)
            file.close()
        with open('../{}/blocking_bug_pairs.json'.format(repo),'w',encoding='utf8') as file:
            json.dump(list(blocking_bug_pairs),file)
            file.close()

def get_rq1_metrics(repos):
    for repo in repos:    
        files=os.listdir('../{}/data/'.format(repo))
        
        header=['bug','CC_Count','Comment_Count','Developer_Count']
        file=open('../{}/RQ1/metrics.csv'.format(repo),'w',newline='',encoding='utf8')
        file_csv=csv.DictWriter(file,header)
        file_csv.writeheader()
        
        for file in files:
            print(file)
            path='../{}/data/'.format(repo)+file
        
            soup = BeautifulSoup(open(path,encoding='utf8'),"xml")
        
            ccs=soup.find_all("cc")
            
            developers=[]
            for cc in ccs:
                developers.append(cc.string)
            whos=soup.find_all("who")
            for who in whos:
                developers.append(who.string)
            reporter=soup.find_all("reporter")
            for r in reporter:
                developers.append(r.string)
            assign=soup.find_all("assigned_to")
            for a in assign:
                developers.append(a.string)
            comments=soup.find_all("comment_count")
            if(len(comments)==0):
                commentids=soup.find_all('commentid')
                if(len(commentids)==0):
                    comment_count=0
                else:
                    comment_count=len(commentids)-1
            else:
                comment_count=comments[-1].string
            file_csv.writerow({'bug':file.split('.')[0][1:],'CC_Count':len(ccs),'Comment_Count':comment_count,'Developer_Count':len(set(developers))})


def get_activity(path,repo):
    resolve_time=[]
    fix_time=[]
    assign_time=[]
    reopen_time=[]
    verified_time=[]
    resolve_dev=[]
    fix_dev=[]
    assign_dev=[]
    reopen_dev=[]
    verified_dev=[]
    soup=BeautifulSoup(open(path,encoding='utf8').read(),'html.parser')
    if(not soup.table):
        return (assign_time,fix_time,reopen_time,resolve_time,verified_time,assign_dev,fix_dev,reopen_dev,resolve_dev,verified_dev)
    #print(soup)
    if(repo=='netbeans'):
        if(not soup.table.table):
            return (assign_time,fix_time,reopen_time,resolve_time,verified_time,assign_dev,fix_dev,reopen_dev,resolve_dev,verified_dev)
        table=soup.table.table
    elif(repo=='openoffice' or repo=='GNOME'):
        tables=soup.find_all('table')
        table=tables[-1]
    else:
        table=soup.table
    
    #print(repo,table)
    trs=table.find_all('tr')  
    
    for i in range(1,len(trs)):
        
        tds=trs[i].find_all("td")
        
        if(len(tds)==5):
            
            people=tds[0].get_text().strip()
            time=tds[1].get_text().strip()
            
            if(tds[2].get_text().strip()=='Assignee'):
                assign_time.append(time)
                assign_dev.append(tds[4].get_text().strip())
            if(tds[4].get_text().strip()=='FIXED'):
                fix_time.append(time)
                fix_dev.append(people)
            if(tds[4].get_text().strip()=='REOPENED'):
                reopen_dev.append(people)
                reopen_time.append(time)
            if(tds[4].get_text().strip()=='RESOLVED'):
                resolve_dev.append(people)
                resolve_time.append(time)
            
        else:
            if(tds[0].get_text().strip()=='Assignee'):
                assign_time.append(time)
                assign_dev.append(tds[2].get_text().strip())
            if(tds[2].get_text().strip()=='FIXED'):
                fix_time.append(time)
                fix_dev.append(people)
            if(tds[2].get_text().strip()=='REOPENED'):
                reopen_dev.append(people) 
                reopen_time.append(time)
            if(tds[2].get_text().strip()=='VERIFIED'):
                verified_time.append(time)
                verified_dev.append(people)
            
    return(fix_time,reopen_time,resolve_time,assign_dev,fix_dev,reopen_dev,resolve_dev)
    

def get_rq2_metrics(repos):

    for repo in repos:
        
        header=['bug','fix_time','reopen_time','resolve_time','assign_dev','fix_dev','reopen_dev','resolve_dev']
        file=open('../{}/RQ2/bug_activity.csv'.format(repo),'w',newline='',encoding='utf8')
        file_csv=csv.DictWriter(file,header)
        file_csv.writeheader()
        
        
        for file in os.listdir('../{}/data/'.format(repo)):
            print(repo,file,file[1:-4])
            path='../{}/new_activity/a{}.htm'.format(repo,file[1:-4])
            #path='../{}/data/'.format(repo)+file
            fix_time,reopen_time,resolve_time,assign_dev,fix_dev,reopen_dev,resolve_dev=get_activity(path,repo)
            file_csv.writerow({'bug':file[1:-4],'fix_time':'#'.join(fix_time),'reopen_time':'#'.join(reopen_time),'resolve_time':'#'.join(resolve_time),'assign_dev':'#'.join(assign_dev),'fix_dev':'#'.join(fix_dev),'reopen_dev':'#'.join(reopen_dev),'resolve_dev':'#'.join(resolve_dev)})
           
def process_rq2_metrics(repos):
    
    for repo in repos:
        header=['bug','fix_time','reopen_time','resolve_time','assign_dev','fix_dev','reopen_dev','resolve_dev']
        file=open('../{}/RQ2/metrics.csv'.format(repo),'w',newline='',encoding='utf8')
        file_csv=csv.DictWriter(file,header)
        file_csv.writeheader()
        
        report_time={}
        with open('../{}/RQ2/bug_report_time.csv'.format(repo),'r',encoding='utf8') as file:
            reader=csv.DictReader(file)
            for row in reader:
                report_time[row['bug']]=row['report_time']
            file.close()
        
        with open('../{}/RQ2/bug_activity.csv'.format(repo),'r',encoding='utf8') as file:
            reader=csv.DictReader(file)
            for row in reader:
                if(row['assign_dev']):
                    assign=len(row['assign_dev'].split('#'))
                else:
                    assign=0
                if(row['fix_dev']):
                    fix=len(row['fix_dev'].split('#'))
                else:
                    fix=0
                if(row['reopen_dev']):
                    reopen=len(row['reopen_dev'].split('#'))
                else:
                    reopen=0
                if(row['resolve_dev']):
                    resolve=len(row['resolve_dev'].split('#'))
                else:
                    resolve=0
                
                bug=row['bug']
                r_time=report_time[bug]
                if(not r_time):
                    file_csv.writerow({'bug':bug,'fix_time':'#','reopen_time':'#','resolve_time':'#','assign_dev':assign,'fix_dev':fix,'reopen_dev':reopen,'resolve_dev':resolve})
                    continue
                print(r_time)
                r_time=datetime.strptime(' '.join(r_time.split(' ')[0:2]),"%Y-%m-%d %H:%M:%S")
                print(bug,r_time)
                
                fix_time=row['fix_time'].split('#')[-1] 
                if(fix_time):
                    fix_time=datetime.strptime(' '.join(fix_time.split(' ')[0:2]),"%Y-%m-%d %H:%M:%S")
                    fix_diff=(fix_time-r_time).days
                else:
                    fix_diff='#'
                
                reopen_time=row['reopen_time'].split('#')[-1]
                if(reopen_time):
                    reopen_time=datetime.strptime(' '.join(reopen_time.split(' ')[0:2]),"%Y-%m-%d %H:%M:%S")
                    reopen_diff=(reopen_time-r_time).days
                else:
                    reopen_diff='#'
                    
                resolve_time=row['resolve_time'].split('#')[-1]
                if(resolve_time):
                    resolve_time=datetime.strptime(' '.join(resolve_time.split(' ')[0:2]),"%Y-%m-%d %H:%M:%S")
                    resolve_diff=(resolve_time-r_time).days
                else:
                    resolve_diff='#'
                    
                file_csv.writerow({'bug':bug,'fix_time':fix_diff,'reopen_time':reopen_diff,'resolve_time':resolve_diff,'assign_dev':assign,'fix_dev':fix,'reopen_dev':reopen,'resolve_dev':resolve})
            file.close()

def match_bug_to_commits(repos):
    
    for repo in repos:
        
        bug_ids=[]
        for root,dirs,files in os.walk('../{}/data'.format(repo)):
            for file in files:
                bug_ids.append(file.split('.')[0][1:])
        formats=['bug[# \s]*([0-9]+)\w*','\[([0-9]+)\]','show\_bug\.cgi\?id=[0-9]+','pr[# \s]*[0-9]+','[\s #]*(\d+)[:\s-]+','[#io]+(\d+)[#:]*']
        commit_path='../{}/RQ3/new_commit_info.csv'.format(repo)
        commit_data=pd.read_csv(commit_path,encoding = 'utf-8')
        
        commits=list(set(list(commit_data['commit'])))
        print(len(commits))
        
        commit_info=dict(zip(commit_data['commit'],commit_data['description']))
        #for i in range(len(commit_data)):
        print(len(commit_info)) 
        
        file=open('../{}/rq3/new_commit_to_bug.csv'.format(repo),'w',newline='',encoding='utf8')
        header=['commit','bug']
        file_csv=csv.DictWriter(file,header)
        file_csv.writeheader()
        
        blk_bug_path='../{}/{}_blocking_bugs.csv'.format(repo,repo)
        data=pd.read_csv(blk_bug_path)
        exist_bugs=list(data['up_bug'])
        exist_bugs.extend(list(data['down_bug']))
        
        file=open('../{}/rq3/new_commit_to_bug.txt'.format(repo),'w')
        count=0
        total_ids=[]
        bug_commit={}
        commit_ids=[]
        for commit in commits:
            info=str(commit_info[commit]).lower()
            #print(info)
            exist_ids=[]
            for i in range(len(formats)):
                pattern = re.compile(formats[i])
                match=pattern.findall(info)
                for m in match:
                    exist_ids.append(m)
            
            real_ids=[]
            for i in set(exist_ids):
                if(i in bug_ids):
                    real_ids.append(i)
                    total_ids.append(i)
                    file_csv.writerow({'commit':commit,'bug':i})
                    file.write(i+' '+commit)
                    file.write('\n')
                    
                    if(i in exist_bugs):
                        print(i)
                    
                    if(i in bug_commit.keys()):
                        bug_commit[i].append(commit)
                    else:
                        temp=[]
                        temp.append(commit)
                        bug_commit[i]=temp
            
            commit_ids.append(real_ids)
            if(len(real_ids)!=0):
                count+=1
        
        print('commit',len(commits),count)
        print('bug',len(bug_ids),len(set(total_ids)),len(set(total_ids))/len(bug_ids))
        counts=[]
        for key,value in bug_commit.items():
            counts.append(len(value))
        print(len(counts),max(counts),min(counts))
        print(counts.count(1))  

    
if __name__=='__main__':
    
    all_repos=['eclipse','freedesktop','mozilla','netbeans','openoffice']
    #get_blocking_bugs(all_repos)
    #get_breakable_blocking_bugs(all_repos)
    
    #get_rq1_metrics(all_repos)
    
    
    #get_rq2_metrics(all_repos)
    #process_rq2_metrics(all_repos)
    
    
    #match_bug_to_commits(all_repos)
    
    