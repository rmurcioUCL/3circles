
setwd(paste0(Sys.getenv('CS_HOME'),'/UrbanDynamics/Models/MobilityPlaces/juste'))

source(paste0(Sys.getenv('CS_HOME'),'/Organisation/Models/Utils/R/plots.R'))

library(sf)
library(cartography)
library(dplyr)
library(ggplot2)
library(igraph)


msoa = st_read(dsn = '../London_Data/ESRI',layer='MSOA_2011_London_gen_MHW')

flows = as.tbl(read.csv('../../../Data/Foursquare/movements_v2/London_movements_v2.csv',header=F))
names(flows)<-c('from','to','month','window','count')

flows$id = paste0(flows$from,flows$to)

counts = flows %>% group_by(id,month) %>% summarize(count=n())

venues = as.tbl(read.csv('../../../Data/Foursquare/venues_v2/London_venue_info_v2.csv'))
venuepoints=list();for(i in 1:nrow(venues)){venuepoints[[i]]=st_point(as.matrix(venues[i,c("lng","lat")]))}
venuesf = st_sf(venues,geometry=venuepoints)

st_crs(venuesf) <- "+proj=longlat +datum=WGS84"
venuesf = venuesf %>% st_transform(st_crs(msoa))

# overlay venues to msoas
overlay <- st_join(venuesf, msoa, join = st_intersects)

# join to flows
from_over_flows = left_join(flows,overlay[,c('id','MSOA11CD')],by=c('from'='id'))
names(from_over_flows)[6]<-"from_msoa"
to_over_flows = left_join(flows,overlay[,c('id','MSOA11CD')],by=c('to'='id'))
names(to_over_flows)[6]<-"to_msoa"
over_flows = from_over_flows
over_flows$to_msoa = to_over_flows$to_msoa

# compute distancein flow mat ?




# map aggreg flows
sflows <- over_flows %>% group_by(from_msoa,to_msoa) %>% summarize(count=sum(count))

reg = lm(data=data.frame(rank=log(1:nrow(sflows)),flow=log(sort(sflows$count,decreasing = T))),flow~rank)
summary(reg)
g=ggplot(data.frame(rank=1:nrow(sflows),flow=sort(sflows$count,decreasing = T)),aes(x=rank,y=flow))
g+geom_point()+#geom_smooth(color='red',linewidth=0.1)+
  ggtitle(paste0('Linear adj. R2 = ',format(summary(reg)$adj.r.squared,digits=3)))+
  scale_x_log10()+scale_y_log10()+xlab('Rank')+ylab('Flow (aggregated count)')+stdtheme
ggsave(file='Results/ranksize_aggregflows.png',width=20,height=18,units='cm')

# up to the median flows are noise !

threshold = 0.99
fsflows = sflows[sflows$count>quantile(sflows$count,threshold),]
fsflows$id = paste0(fsflows$from_msoa,fsflows$to_msoa)
fsflows$linktype = rep("aggreg",nrow(fsflows))

links <- getLinkLayer(x=msoa,xid='MSOA11CD',fsflows,dfid = c("from_msoa","to_msoa"))
links$id = paste0(links$from_msoa,links$to_msoa)
links = left_join(links,fsflows[,c('id','count')])


png(filename = "Results/map_aggreg_flows.png",width = 40, height = 35, units = "cm",res=300)
plot(st_geometry(msoa), col = "grey13", border = "grey25", bg = "grey25", lwd = 0.5)
gradLinkTypoLayer(
  x = links,
  df = fsflows,
  var = "count", 
  breaks = c( min(fsflows$count),  quantile(fsflows$count,c(0.25)), median(fsflows$count), quantile(fsflows$count,c(0.995)), quantile(fsflows$count,c(0.9995))),
  lwd = c(0.5,1,2,5),
  var2 = "linktype"
) 
layoutLayer(title = "Aggregated flows between MSOA",
            frame = FALSE, col = "grey25", coltitle = "white",
            tabtitle = TRUE)
dev.off()


######
# try to map by window of the day

sflows <- over_flows %>% group_by(from_msoa,to_msoa,window) %>% summarize(count=sum(count))

threshold = 0.99
fsflows = sflows[sflows$count>quantile(sflows$count,threshold),]
fsflows$id = paste0(fsflows$from_msoa,fsflows$to_msoa)

links <- getLinkLayer(x=msoa,xid='MSOA11CD',fsflows,dfid = c("from_msoa","to_msoa"))
links$id = paste0(links$from_msoa,links$to_msoa)
links = left_join(links,fsflows[,c('id','count')])


png(filename = "Results/map_aggreg_flows_bywindow.png",width = 40, height = 35, units = "cm",res=300)
plot(st_geometry(msoa), col = "grey13", border = "grey25", bg = "grey25", lwd = 0.5)
gradLinkTypoLayer(
  x = links,
  df = fsflows,
  var = "count", 
  breaks = c( min(fsflows$count),  quantile(fsflows$count,c(0.25)), median(fsflows$count), quantile(fsflows$count,c(0.995)), quantile(fsflows$count,c(0.9995))),
  lwd = c(0.5,1,2,5),
  var2 = "window",
  col = gg_color_hue(length(unique(fsflows$window)))
) 
layoutLayer(title = "Aggregated flows between MSOA",
            frame = FALSE, col = "grey25", coltitle = "white",
            tabtitle = TRUE)
dev.off()



######
# network topology in time

# aggreg to graph
sflows <- over_flows %>% group_by(from_msoa,to_msoa,window,month) %>% # filter(!is.na(from_msoa)&!is.na(to_msoa)) %>%
  summarize(count=sum(count))
sflows$from_msoa = as.character(sflows$from_msoa);sflows$to_msoa = as.character(sflows$to_msoa)
sflows = sflows %>% filter(!is.na(from_msoa)&!is.na(to_msoa))
sflows$weight = sflows$count
sflows$count = NULL

graph <- graph_from_data_frame(as.data.frame(sflows))

computeGraphMeasures <- function(g){
  degs = degree(g ,normalized = T)
  avgDeg = mean(degs)
  degs = degs[degs>median(degs)]
  alphaDeg = summary(lm(data=data.frame(rank=log(1:length(degs)),deg=log(sort(degs,decreasing = T))),deg~rank))$adj.r.squared
  return(c(avgDeg=avgDeg,alphaDeg=alphaDeg))
}

measures=c()
for(month in unique(E(graph)$month)){
  show(month)
  currentgraph = subgraph.edges(graph,which(E(graph)$month==month))
  mes = computeGraphMeasures(currentgraph)
  measures=append(measures,c(value=mes['avgDeg'],var='avgDeg',month=month))
  measures=append(measures,c(value=mes['alphaDeg'],var='alphaDeg',month=month))
}

measuresdf=data.frame()
names(measures)=c('value','var','month')
measures$value<- as.numeric(measures$value)

g=ggplot(measures,aes(x=month,y=value,color=var,group=var))
g+geom_point()+geom_line()











