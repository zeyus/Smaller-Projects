#Make sure you're in the folder where your data is
getwd()
setwd("/Users/FlowersnIce-cream/Google Drev/Hogwarts/4/Models for perception and action/Exam/3 - Movements/W13 - Motion tracking and analysis/Exp/")


#df, long format data - The data we used the first week

load("MT_Pilot20190314.R") 

df <- subset(df, ID == unique(df$ID)[1] & GainLoss == unique(df$GainLoss)[1] & Trial == unique(df$Trial)[1] )
#df <- df[85:91,]

#calculate euclidian distance....
correct_manualdist <- sum(sqrt(diff(df$Pos_x)^2 + diff(df$Pos_y)^2))
correct_manualdist





################

#same data but rearranged to fit the mousetrap package
#mt, list object 
load("MTrap_Pilot20190314.R") 


#What does the data look like
head(mt[[1]])
mt[[2]][1:10,1:10,1]
names(mt[[2]][1,1,]) #what dimensions do I have?
head(mt[[2]][1,,])




#Calculate euclidian distance
library("mousetrap")
mt[[2]] <- mt_derivatives(mt[[2]]) #

#What did we get?
head(mt[[2]][1,,])


#calculate trial-wise/per trajectory measures (based on mt_id)
measures <- mt_measures(mt[[2]])  
#what did we get?
head(measures) 



#compare manual distance measure
#although measures are already trial-by-trial we aggregate again over trial since mt_id is not in df
per_trial <- mt_aggregate(measures, use2 = mt[[1]], use2_variables = c("ID", "GainLoss", "Trial", "Volatility"))
head(per_trial)
mousetrap_dist <-per_trial$total_dist[match(paste0(df$ID[1], df$GainLoss[1], df$Trial[1]), 
                                   paste0(per_trial$ID, per_trial$GainLoss, per_trial$Trial))]

#what distance measures did we get?
mousetrap_dist
correct_manualdist
mousetrap_dist == correct_manualdist






#simple test on data aggregated per subject and conditions
#(I would usually not aggregate over trials but for the sake of simplicity...)
per_subject <- mt_aggregate(measures, use2 = mt[[1]], use2_variables = c("ID", "GainLoss","TestCondition", "Volatility"))
per_subject_testgain <- subset(per_subject, GainLoss == "Gain" & TestCondition == 1)
head(per_subject_testgain)

#I just start with plotting a bit
library("ggplot2")
ggplot(per_subject_testgain, aes(x = total_dist, stat(density), color = Volatility)) +
  geom_freqpoly(binwidth = 40)
#log transformation would make it slightly more normal ()
ggplot(per_subject_testgain, aes(x = log(total_dist), stat(density), color = Volatility)) +
  geom_freqpoly(binwidth = 0.1)

#simplest test possible
t.test(log(total_dist)~Volatility, data = per_subject_testgain, paired = T)  




###Visualization

mt_plot(mt[[2]])
mt_plot(mt[[2]], use = "trajectories", use2 = mt[[1]], facet_row = "Volatility", 
        facet_col= "GainLoss")



#Subsetting (can't make the mt_subset to work...)
#Easier data to play around with
mtsubset_ids <- mt[[1]]$TestCondition == 1 & mt[[1]]$GainLoss == "Gain"
mtsub <- mt[[2]][mtsubset_ids,,]
mt_plot(mtsub, use = "trajectories", use2 = mt[[1]][mtsubset_ids,], facet_col = "Volatility")



#identifying and plotting 4 clusters
#it is necessary to have an equal number of observations per trajectory.
spatial <- mt_spatialize(mtsub)
cluster_test <- mt_cluster(spatial, n_cluster = 4, use = "sp_trajectories")  #takes long time
mt_plot(spatial, use="trajectories", use2 = cluster_test, facet_col="cluster")



mt_heatmap(mt[[2]], bounds = c(-400, -50, 400, 450))



