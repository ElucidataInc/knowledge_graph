##Geo_adaptor R code

if(!require("Require")){
    install.packages("Require") 
    library(Require)
}
##installing required packages
Require::Require(packageVersionFile = "mySnapshot.txt")

library(yaml)
library(MetaVolcanoR)
library(htmlwidgets)
library(ggplot2)
library(pander)
library(dplyr)
library("readr")

f=c()
##loading configuration yml file
config = yaml.load_file("config.yml")

##creating directory for geo
dir.create(file.path(config$db$dir), showWarnings = FALSE)
setwd(file.path(config$db$dir))

csvdir=config$db$csvdir

diffexplist = list()
list1=list()
for (i in list.files(path=csvdir, pattern=".csv", all.files=TRUE,full.names=TRUE)){
  nam=tools::file_path_sans_ext(i)
  print(i)
  df=read.csv(file.path(i))
  df<- subset(df, select = -c(AveExpr))
  ##naming dataframe from csv file name(removing file extension)
  list1 [[nam]]=df
  ##creating a list of dataframes
  diffexplist=append(diffexplist,list1)
}

##meta analysis combining pvalue by fishers method and log2fc by mean value
meta_degs_comb <- combining_mv(diffexp=diffexplist,
                               pcriteria='PValue', 
                               foldchangecol='log2FC',
                               genenamecol='Gene',
                               geneidcol=NULL,
                               metafc='Mean',
                               metathr=0.01, 
                               collaps=TRUE,
                               jobname="MetaVolcano",
                               outputfolder=".",
                               draw='PDF')

##threshold values for pvalue and log2fc from configuration file
pthr=config$db$pvaluethr
logthr=config$db$log2fcthr 
disease=config$db$disease

aux = which(meta_degs_comb@metaresult[,'metap'] < pthr)
##getting subset of upregulated genes 
auxup = aux[which( meta_degs_comb@metaresult[aux,'metafc'] > logthr)]
##getting subset of downregulated genes 
auxdown = aux[which(meta_degs_comb@metaresult[aux,'metafc'] < -logthr)]

##creating dataframe for upregulated genes
df_up=data.frame(Gene=meta_degs_comb@metaresult[auxup,"Gene"],metap=meta_degs_comb@metaresult[auxup,"metap"],metafc=meta_degs_comb@metaresult[auxup,"metafc"])
df_up$Disease <-  rep(c(disease))
df_up = df_up %>% select(Disease, Gene, metap,metafc)

##creating a dataframe for downregulated genes
df_down=data.frame(Gene=meta_degs_comb@metaresult[auxdown,"Gene"],metap=meta_degs_comb@metaresult[auxdown,"metap"],metafc=meta_degs_comb@metaresult[auxdown,"metafc"])
df_down$Disease <-  rep(c(disease))
df_down = df_down %>% select(Disease,Gene,metap,metafc)

up=config$db$upregulatedfile
down=config$db$downregulatedfile
# Writing up and down regulated dataframe  data to a tsv file
write_tsv(df_up, file = up)
write_tsv(df_down, file = down)

