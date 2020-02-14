

source("loaddata.R")
source("deps.R")

# subset home and away
away <- matches %>% subset(Side=="away")
home <- matches %>% subset(Side=="home")

# subset coaches
coach1 <- matches %>% subset(CoachID=="Coach1")
coach2 <- matches %>% subset(CoachID=="Coach2")
coach3 <- matches %>% subset(CoachID=="Coach3")

c1Stats=factor(coach1$Outcome)
c2Stats=factor(coach2$Outcome)
c3Stats=factor(coach3$Outcome)

away=factor(away$Outcome)
home=factor(home$Outcome)

homeAwayRes=rbind(away=table(away), home=table(home))
homeAwayRes2=rbind(homeAwayRes,colSums(homeAwayRes))

homeAwayRatios <- homeAwayRes/rbind(colSums(homeAwayRes), colSums(homeAwayRes))


coachRes <- rbind(Coach1=table( Coach1=c1Stats ),
                  Coach2=table( Coach2=c2Stats ),
                  Coach3=table( Coach3=c3Stats ))
coachRes

