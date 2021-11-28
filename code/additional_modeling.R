emotion_data_child$Age <- as.numeric(emotion_data_child$Age)
emotion_data_child$Total_ratio <- as.numeric(emotion_data_child$Total_ratio)


#emotion_logistic <- brm(formula = Total_ratio ~ log(Age) + Polarity,
#    data = emotion_data_child, 
#    family = gaussian(),
#    control = list(adapt_delta = 0.9))


#emotion_child_neg_nonlinear_simple <- brm(
#  bf(Total_ratio ~ ult * (1 - exp(-(Age/theta)^omega)),
#     ult ~ 1, omega ~ 1, theta ~ 1, nl = TRUE),
#  data = subset(emotion_data_child, Polarity == 'negative'), family = gaussian(),
#  prior = c(
#    prior(normal(0, 1), nlpar = "ult"),
#    prior(normal(0, 1), nlpar = "omega"),
#    prior(normal(0, 2), nlpar = "theta")
#  ),
#  control = list(adapt_delta = 0.9))


### Weibull distribution cumulative curve ###

emotion_child_neg_weibull <- brm(
  bf(Total_ratio ~ (omega/scale) * (((Age - location) / scale)^(omega-1)) * (exp(-1 * (((Age - location) / scale)^omega))),
     omega + location + scale ~ 1, nl = TRUE),
  data = subset(emotion_data_child, Polarity == 'negative'), 
  prior = c(
    prior(normal(0, 1), nlpar = "scale"),
    prior(normal(0, 1), nlpar = "omega"),
    prior(normal(0, 2), nlpar = "location")
  ),
  control = list(adapt_delta = 0.9, max_treedepth = 15),
  iter = 3000)


emotion_child_neg_weibull <- brm(
  bf(Total_ratio ~ (omega/scale) * (((Age - location) / scale)^(omega-1)) * (exp(-1 * (((Age - location) / scale)^omega))),
     omega + location + scale ~ 1, nl = TRUE),
  data = subset(emotion_data_child, Polarity == 'negative'), family = gamma(),
  prior = c(
    prior(student_t(3, 1, 1), nlpar = "scale"),
    prior(student_t(3, 1, 1), nlpar = "omega"),
    prior(student_t(3, 1, 1), nlpar = "location")
  ),
  control = list(adapt_delta = 0.9),
  iter = 3000)

### logistic growth curve ###

#growthcurve <- function(t, omega, theta) t^omega/(t^omega + theta^omega)

#curve(growthcurve(x, 2, 4)*100, from = 0, to = 10, bty="n", ylim=c(0,100),
#      main="Log-logistic gowth curve", ylab="% developed", xlab="Development period")


logistic_priors <- c(
  prior(lognormal(log(0.6), log(2)), nlpar = "ulr", lb=0),
  prior(normal(0, 1), nlpar = "omega", lb=0),
  prior(normal(0, 1), nlpar = "theta", lb=0))
#  prior(student_t(3, 0, 1), class = "sigma"),
#  prior(student_t(3, 0, 1), class = "sd", nlpar = "omega"),
#  prior(student_t(3, 0, 1), class = "sd", nlpar = "theta"),
#  prior(student_t(3, 0, 1), class = "sd", nlpar = "ulr"),
#  prior(lkj(2), class="cor"))

emotion_child_neg_logistic_formula <- bf(Total_ratio ~ log(ulr * Age^omega/(Age^omega + theta^omega)),
                                         ulr + omega + theta ~ 1,
                                         #     ulr ~ 1 +  (1|ID|entity_name) + (1|origin_year:entity_name) ,
                                         #     omega ~ 1 + (1|ID|entity_name),
                                         #     theta ~ 1 + (1|ID|entity_name),
                                         nl = TRUE)


emotion_child_neg_logistic <- 
  brm(emotion_child_neg_logistic_formula, 
      data = subset(emotion_data_child,Polarity=='negative'), 
      prior = logistic_priors, 
      seed = 1234,
      family = lognormal(link = "identity", link_sigma = "identity"),
      control = list(adapt_delta = 0.999, max_treedepth=15))

emotion_child_logistic_formula <- bf(Total_ratio ~ log(ulr * Age^omega/(Age^omega + theta^omega)),
                                     ulr ~ 1 +  (1|Polarity),
                                     omega ~ 1 + (1|Polarity),
                                     theta ~ 1 + (1|Polarity),
                                     nl = TRUE)

emotion_child_logistic <- 
  brm(emotion_child_logistic_formula, 
      data = emotion_data_child, 
      prior = logistic_priors, 
      seed = 1234,
      family = lognormal(link = "identity", link_sigma = "identity"),
      control = list(adapt_delta = 0.999, max_treedepth=15))

p1 <- conditional_effects(emotion_child_neg_nonlinear, 
                          effects = "Age",
                          int_conditions = list(shade_cent = 12:72))

plot(p1,
     plot = F)[[1]] +
  scale_x_continuous(breaks = seq(0, 72, 6)) +
  ylab('production ratio') + 
  xlab('child age (moths)') + 
  theme(legend.position = "none",
        panel.grid.minor = element_blank()) +
  theme_classic()

emotion_child_pos_nonlinear <- brm(
  bf(Total_ratio ~ ult * (1 - exp(-(Age/theta)^omega)),
     ult ~ 1, omega ~ 1, theta ~ 1, nl = TRUE),
  data = subset(emotion_data_child, Polarity == 'positive'), family = gaussian(),
  prior = c(
    prior(normal(5000, 1000), nlpar = "ult"),
    prior(normal(1, 2), nlpar = "omega"),
    prior(normal(45, 10), nlpar = "theta")
  ),
  control = list(adapt_delta = 0.9))

p2 <- conditional_effects(emotion_child_pos_nonlinear, 
                          effects = "Age",
                          int_conditions = list(shade_cent = 12:72))

plot(p2,
     plot = F)[[1]] +
  scale_x_continuous(breaks = seq(0, 72, 6)) +
  ylab('production ratio') + 
  xlab('child age (moths)') + 
  theme(legend.position = "none",
        panel.grid.minor = element_blank()) +
  theme_classic()