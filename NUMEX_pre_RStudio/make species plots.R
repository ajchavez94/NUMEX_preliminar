make_species_plots <- function(yvar, y_label = yvar, y_limits = c(0, 150)) {
  
  # dynamic column reference
  ycol <- rlang::sym(yvar)
  
  make_one_plot <- function(species_name) {
    
    df <- data[data$name == species_name, ]
    
    # mean of control
    mean_control <- mean(df[df$SUB == "C", ][[yvar]], na.rm = TRUE)
    
    ggplot(df, aes(x = SUB, y = !!ycol, colour = SUB)) +
      
      geom_boxplot(aes(group = SUB),
                   colour = "black",
                   fill = "grey90",
                   alpha = 0.5) +
      
      geom_hline(yintercept = mean_control,
                 colour = "black",
                 linetype = "dotted",
                 linewidth = 1) +
      
      geom_jitter(width = 0.2, alpha = 0.6) +
      
      annotate("label",
               x = 4, y = y_limits[2] - 1,
               label = "test",#HELP
               fill = "white",
               colour = "black",
               size = 3) +
      
      scale_y_continuous(limits = y_limits) +
      
      labs(title = bquote(italic(.(species_name))),
           x = "",
           y = y_label) +
      
      theme_bw() +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))
  }
  
  # Build 6 plots
  p_list <- lapply(species_order, make_one_plot)
  
  final_plot <- ((p_list[[1]] | p_list[[2]] | p_list[[3]]) /
                   (p_list[[4]] | p_list[[5]] | p_list[[6]])) +
    plot_layout(guides = "collect") &
    theme(legend.position = "bottom")
  
  #ggsave(filename= paste0("species_boxplots_", y_label,".png"),
  #       plot = final_plot,
  #       width = 10, height = 10, units = "in", dpi = 300)
  
  return(final_plot)
}