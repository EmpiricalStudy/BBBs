library(ggplot2)
library(cowplot)

repos <- c('eclipse','freedesktop','mozilla','netbeans','openoffice')


for (repo in repos){
  file_path <- paste('D:/breakable-blocking-bugs',repo,'RQ1','rq1_dataset.CSV',sep='/')
  
  file_datas <-read.csv(file_path,header = TRUE)
  metrics_datas<-file_datas[file_datas$metric %in% c('fix_time','reopen_time','resolve_time'),]
  metric.labs<-c('Fix Time','Reopen Time','Resolve Time')
  names(metric.labs)<-c('fix_time','reopen_time','resolve_time')
  
  metrics_datas<-file_datas[file_datas$metric %in% c('fix_time'),]
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  p2 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  p2<-p2+coord_cartesian(ylim=c(0,600))
  p2 <- p2+theme(text=element_text(size=25),axis.text.x = element_blank(),legend.position ='None',axis.title.x = element_blank(),axis.title.y = element_blank())
  metric.labs<-c('Fix_Time')
  names(metric.labs)<-c('fix_time')
  p2<-p2+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs,project=project.labs))
  
  
  metrics_datas<-file_datas[file_datas$metric %in% c('reopen_time'),]
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  p3 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  p3<-p3+coord_cartesian(ylim=c(0,800))
  p3 <- p3+theme(text=element_text(size=25),strip.text.x = element_blank(),axis.text.x = element_blank(),legend.position ='None',axis.title.x = element_blank(),axis.title.y = element_blank())
  metric.labs<-c('Reopen_Time')
  names(metric.labs)<-c('reopen_time')
  p3<-p3+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs,project=project.labs))
  
  
  metrics_datas<-file_datas[file_datas$metric %in% c('resolve_time'),]
  print(summary(metrics_datas[metrics_datas$type=='Breakable Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Normal Blocking Bug',]))
  print(summary(metrics_datas[metrics_datas$type=='Other Bug',]))
  p4 <- ggplot(metrics_datas,aes(x=factor(type),y=value,fill=type))+ geom_boxplot(outlier.shape = NA)+stat_summary(fun = "mean",geom="point",shape=23,size=2,fill="white")
  p4<-p4+coord_cartesian(ylim=c(0,900))
  p4 <- p4+theme(text=element_text(size=25),strip.text.x = element_blank(),axis.text.x = element_blank(),legend.position ='None',axis.title.x = element_blank(),axis.title.y = element_blank())
  metric.labs<-c('Resolve_Time')
  names(metric.labs)<-c('resolve_time')
  p4<-p4+facet_grid(metric~project,scale="free",labeller = labeller(metric=metric.labs,project=project.labs))
  
  
  p<-plot_grid( p2, p3,p4, ncol = 1,align='vh')
  print(p)
  ggsave('D:/breakable-blocking-bugs/eclipse/RQ1/metric_time_figure.pdf', dpi = 600,width = 12, height = 10)
  
  break
}
