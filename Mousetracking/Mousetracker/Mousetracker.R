setwd("/Users/FlowersnIce-cream/Google Drev/Hogwarts/4/Models for perception and action/Mousetracker")
MT <- load("MT_Pilot20190314.R")
MTtrap <- load("MTrap_Pilot20190314.R")
library(ggplot2)
library(tidyverse)
df <- filter()

df_1 <- filter(df,Trial == 1)
ggplot(df_1, aes(x = Pos_x, y = Pos_y, color=ID)) + geom_point() + facet_wrap(~GainLoss)
ggplot(df_1, aes(x = Pos_x, y = Pos_y)) + geom_point() + facet_wrap(~GainLoss) + geom_smooth(method = lm, , formula = y ~ x + I(x^2), se =F)
df_2 <- filter(df,Trial == 2)
ggplot(df_2, aes(x = Pos_x, y = Pos_y, color=ID)) + geom_point() + facet_wrap(~GainLoss)
ggplot(df_2, aes(x = Pos_x, y = Pos_y)) + geom_point() + facet_wrap(~GainLoss) + geom_smooth(method = lm, , formula = y ~ x + I(x^2), se =F)
df_3 <- filter(df,Trial == 3)
ggplot(df_3, aes(x = Pos_x, y = Pos_y, color=ID)) + geom_point() + facet_wrap(~GainLoss)
ggplot(df_3, aes(x = Pos_x, y = Pos_y)) + geom_point() + facet_wrap(~GainLoss) + geom_smooth(method = lm, , formula = y ~ x + I(x^2), se =F)
df_4 <- filter(df,Trial == 4)
ggplot(df_4, aes(x = Pos_x, y = Pos_y, color=ID)) + geom_point() + facet_wrap(~GainLoss)
ggplot(df_4, aes(x = Pos_x, y = Pos_y)) + geom_point() + facet_wrap(~GainLoss) + geom_smooth(method = lm, , formula = y ~ x + I(x^2), se =F)
df_10 <- filter(df,Trial == 10)
ggplot(df_10, aes(x = Pos_x, y = Pos_y, color=ID)) + geom_point() + facet_wrap(~GainLoss)
ggplot(df_10, aes(x = Pos_x, y = Pos_y)) + geom_point() + facet_wrap(~GainLoss) + geom_smooth(method = lm, , formula = y ~ x + I(x^2), se =F)



df_105955 <- filter(df,Trial == 1, ID == 105955, GainLoss=="Loss")
sum(abs(diff(df_105955$Pos_x))) + sum(abs(diff(df_105955$Pos_y)))

