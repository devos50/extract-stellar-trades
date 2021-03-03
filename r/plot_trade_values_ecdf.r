library(ggplot2)

dat <- read.csv("../trade_values.csv")

p <- ggplot(dat, aes(x=value)) +
     stat_ecdf(geom="step") +
     xlab("Trade value (USD)") +
     ylab("ECDF") +
     theme_bw()

ggsave(filename="trade_values.pdf", plot=p, width=6, height=3)
