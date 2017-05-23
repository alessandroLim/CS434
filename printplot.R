data <- read.csv("C:/Users/aless/Documents/GitHub/CS434/finalres.csv")
data2 <- read.csv("C:/Users/aless/Documents/GitHub/CS434/result.csv")
plot(data, ylab="SSE", xlab="k")

plot(data2, ylab="SSE", main="SSE for k = 2")