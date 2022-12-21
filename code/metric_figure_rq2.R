library(ggplot2)
library(cowplot)


repos <- c('All','eclipse','freedesktop','mozilla','netbeans','openoffice')
for (repo in repos){
  file_path <- paste('D:/breakable-blocking-bugs','eclipse','RQ2','rq2_dataset.CSV',sep='/')
  
  file_datas <-read.csv(file_path,header = TRUE)
  file_datas<-file_datas[file_datas$type %in% c('Blocking Bug','Normal Bug','Breakable Blocking Bug'),]
  file_datas$type<- factor(file_datas$type,levels = c('Breakable Blocking Bug','Blocking Bug','Normal Bug'),labels = c('Breakable Blocking Bug','Normal Blocking Bug','Other Bug'))
  metrics_datas<-file_datas[file_datas$metric %in% c('CountLineCode'),]
  #print(metrics_datas)
  
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  
  p1 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  
  p1<-p1+coord_cartesian(ylim=c(0,2000))
  
  p1 <- p1+theme(text=element_text(size=16),axis.text.x = element_blank(),legend.position ='none',axis.title.x = element_blank(),axis.title.y = element_blank())
  
  
  project.labs<-c('All','Eclipse','FreeDesktop','Mozilla','Netbeans','Openoffice')
  names(project.labs)<-c('All','eclipse','freedesktop','mozilla','netbeans','openoffice')
  metric.labs<-c('Line Count')
  names(metric.labs)<-c('CountLineCode')
  
  p1<-p1+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs,project=project.labs))
  print(p1)
  
  
  metrics_datas<-file_datas[file_datas$metric %in% c('CountDeclFunction'),]
  
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  
  p2 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  
  p2<-p2+coord_cartesian(ylim=c(0,70))
  p2 <- p2+theme(strip.text.x = element_blank(),text=element_text(size=16),axis.text.x = element_blank(),legend.position ='none',axis.title.x = element_blank(),axis.title.y = element_blank())
  metric.labs<-c('Function Count')
  names(metric.labs)<-c('CountDeclFunction')
  
  p2<-p2+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs))
  print(p2)
  
  
  metrics_datas<-file_datas[file_datas$metric %in% c('SumCyclomatic'),]
  
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  
  p5 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  
  p5<-p5+coord_cartesian(ylim=c(0,200))
  p5 <- p5+theme(strip.text.x = element_blank(),text=element_text(size=16),axis.text.x = element_blank(),legend.position ='none',axis.title.x = element_blank(),axis.title.y = element_blank())
  metric.labs<-c('Cyclomatic Count')
  names(metric.labs)<-c('SumCyclomatic')
  
  p5<-p5+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs))
  
  
  metrics_datas<-file_datas[file_datas$metric %in% c('SumEssential'),]
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  
  p6 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  
  p6<-p6+coord_cartesian(ylim=c(0,100))
  p6 <- p6+theme(strip.text.x = element_blank(),text=element_text(size=16),axis.text.x = element_blank(),legend.position ='bottom',axis.title.x = element_blank(),axis.title.y = element_blank())
  metric.labs<-c('Essential Count')
  names(metric.labs)<-c('SumEssential')
  
  p6<-p6+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs))+labs(fill='Bug Type')
  print(p6)
  
  p<-plot_grid(p1, p2,p5,p6, ncol = 1,align='vh')
  print(p)
  ggsave('D:/breakable-blocking-bugs/eclipse/RQ5/total_metric_figure.pdf', dpi = 600,width = 10, height = 8)
  
  break
}