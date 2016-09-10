data= read.table('C:/Users/Platina/Desktop/country year.txt',header=F)
colnames(data)=c('country','year','rating')
library(ggplot2)
ggplot(data,aes(x=year,y=rating))+geom_point(aes(colour=country),size=4)
qplot(data=data,x=year,y=rating,color=country,geom=c('smooth','point'))
abline
