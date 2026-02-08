install.packages("devtools")
install.packages("Rchelsa")

install_git("https://gitlabext.wsl.ch/karger/rchelsa.git")

library("Rchelsa")
library("terra")
library(devtools)


extent <- c(-78.30, -77.90, -0.40, -0.30)            # xmin, xmax, ymin, ymax
startdate <- as.Date("1980-01-01")
enddate   <- as.Date("1980-02-01")

