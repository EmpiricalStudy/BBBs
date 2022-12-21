
library(effsize)

repos <- c('All','eclipse','freedesktop','mozilla','netbeans','openoffice')
metrics<-c('fix_time','reopen_time','resolve_time','assign_count','fix_count','reopen_count','resolve_count')


all_repos<-c()
all_metrics<-c()
bbps<-c()
bbds<-c()
bps<-c()
bds<-c()

for (repo in repos){
  file_path <- paste('D:/breakable-blocking-bugs','eclipse','RQ1','rq1_dataset.CSV',sep='/')
  file_datas <- read.csv(file_path,header = TRUE)
  #print(file_datas)
  
  file_datas=file_datas[file_datas$project==repo,]
  for (metric in metrics){
    metric_datas <- file_datas[file_datas$metric==metric,]
    print(repo)
    print(metric)
      
      
    bbbs=metric_datas[metric_datas$type=='Breakable Blocking Bug',]
    bbs=metric_datas[metric_datas$type=='Normal Blocking Bug',]
    bs=metric_datas[metric_datas$type=='Other Bug',]
    #print(as.numeric(bbbs$value))
    bbp <- wilcox.test(as.numeric(bbbs$value),as.numeric(bbs$value))$p.value
    bbd <- cliff.delta(as.numeric(bbbs$value),as.numeric(bbs$value))$estimate
    
    bp <- wilcox.test(as.numeric(bbbs$value),as.numeric(bs$value))$p.value
    bd <- cliff.delta(as.numeric(bbbs$value),as.numeric(bs$value))$estimate
    
    p_adjust <- p.adjust(c(bbp,bp),method = 'BH')
    
    all_repos<-c(all_repos,repo)
    all_metrics <-c(all_metrics,metric)
    bbps<-c(bbps,p_adjust[1])
    bbds<-c(bbds,bbd)
    bps<-c(bps,p_adjust[2])
    bds<-c(bds,bd)
    #break
    print(repo)
    print(metric)
    print(p_adjust)
    
  } 
  #break
}

data <- data.frame(repo=all_repos,metric=all_metrics,blocking_bug_p_value=bbps,blocking_bug_d_value=bbds,bug_p_value=bps,bug_d_value=bds)
write.csv(data, 'D:/breakable-blocking-bugs/eclipse/RQ1/p_d.csv',sep=',')


