library(ggplot2)

dat <- read.csv("../trade_values.csv")
print(nrow(dat))

dat_filtered <- subset(dat, dat$value <= 100)
print(nrow(dat_filtered))

p <- ggplot(dat_filtered, aes(x=value)) +
     geom_histogram(bins=50) +
     xlab("Trade value (USD)") +
     ylab("ECDF") +
     theme_bw()

ggsave(filename="trade_values.pdf", plot=p, width=6, height=3)


# Trade values per identity
dat <- read.csv("../trade_value_per_identity.csv")
print(nrow(dat))

dat_filtered <- subset(dat, dat$value <= 1000)
print(nrow(dat_filtered))

p <- ggplot(dat_filtered, aes(x=value)) +
     geom_histogram(bins=50) +
     xlab("Trade value (USD)") +
     ylab("ECDF") +
     theme_bw()

ggsave(filename="trade_values_per_identity.pdf", plot=p, width=6, height=3)
