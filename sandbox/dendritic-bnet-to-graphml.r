library(tidyverse)
library(igraph)

here::here("sandbox/dendrite.bnet") |> 
  read_lines() |> 
  enframe(name = NULL, value = "line") |> 
  filter(! str_detect(line, "^#") & str_detect(line, ",[:space:]+")) |> 
  separate(line, into = c("target", "source"), sep = ",") |> 
  slice_tail(n = -1L) |> 
  mutate(across(c(target, source), ~ str_trim(.))) |> 
  mutate(source = str_split(source, pattern = " +\\| +")) |> 
  unnest(source) |> 
  mutate(synergy = as.integer(fct_inorder(source))) |> 
  mutate(source = str_split(source, pattern = "\\&")) |> 
  unnest(source) |> 
  mutate(sign = ifelse(str_detect(source, "^!"), -1L, 1L)) |> 
  mutate(source = str_remove(source, "^!")) |> 
  print() -> dendrite_links
dendrite_links |> 
  select(source, target, everything()) |> 
  graph_from_data_frame(directed = TRUE) |> 
  print() -> dendrite_graph
dendrite_graph |> 
  write_graph(here::here("sandbox/dendrite.gml"), format = "graphml")
