#!/usr/bin/python
#-*- coding: utf-8 -*-

from route.Route import *
#from database.BDD import *
from database.AccessDB import *
from validation.Validation import *
from recup.dataManifest import *
if __name__ == "__main__":
    i = 0
    """Boucle d'arrêt de mon script"""
    while i < 10: 
            """
            Création d'une Route pour faire du SMOOTH
            """
            routeMSS = Route()
            """
            On définit le type de fichier Manifest à recupèrer
            """
            mss = routeMSS.getManifest("CATCHUP", "smooth")
            """
            On télécharge le fichier
            """
            routeMSS.download(mss)
            time.sleep(5)
            """
            Idem pour DASH !
            """
            routeDASH = Route()
            dash = routeDASH.getManifest("CATCHUP", "dash")
            routeDASH.download(dash)
            time.sleep(5)
            """
            Idem pour HLS !
            """
            routeHLS = Route()
            hls = routeHLS.getManifest("CATCHUP", "hls")
            routeHLS.download(hls)
            print ("\n")
            """
            On choisit les 4 derniers fichiers à traiter dans une LISTE
            """
            listeMSS  = routeMSS.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/MSS")
            listeDASH = routeDASH.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/DASH")
            listeHLS  = routeHLS.getLastXMLFile("/home/adama/NetBeansProjects/ABSTRACT1_0/abstract1_0/manifests/dynamic/HLS")
            """
            TRAITEMENT DE CHAQUE FICHIER DE MES DIFFÉRENTES LISTES
            """
            for element in listeMSS:
                manifest = DataManifestMSS(element)
                """
                Instance de ma Base de données
                """
                myInstance = AccessDB("192.168.134.122", "adama", "adama", "ABSTRACT")
                """
                Validation du fichier Manifest avec le schéma donné
                """
                if manifest.validManifest()== True:
                    """
                    fiche = manifest.getAttribSmoothStreamingMedia()
                    manifest.viewDictionary(fiche)
                    liste = manifest.getAttribStreamIndex()
                    for e in liste:
                        manifest.viewDictionary(e)
                    """
                    """ Nom du fichier dans le système """
                    NameSmooth = element.split("/")
                    NameSmooth= NameSmooth[len(NameSmooth)-1]
                    
                    length = len(NameSmooth)
                    dateSup = NameSmooth[19:length]
                    conv=time.strptime(dateSup,"%Y%m%d%H%M%S")
                    dateSup= time.strftime("%Y-%m-%d %H:%M:%S",conv)
                    streamer = NameSmooth[12:18]
                    """
                    TESTS & BDD
                    """
                    majorV = manifest.getAttribSmoothStreamingMedia("MajorVersion")
                    myInstance.selectManifestData("MajorVersion")
                    myInstance.insertSmoothAttr("major_version",str(majorV),str(streamer),str(dateSup))
                    
                    minorV = manifest.getAttribSmoothStreamingMedia("MinorVersion")
                    myInstance.selectManifestData("MinorVersion")
                    myInstance.insertSmoothAttr("minor_version",str(minorV),str(streamer),str(dateSup))
                    
                    duree = manifest.getAttribSmoothStreamingMedia("Duration")
                    myInstance.selectManifestData("Duration")
                    myInstance.insertSmoothAttr("duration",str(duree),str(streamer),str(dateSup))
                    """
                    dvr = manifest.getAttribSmoothStreamingMedia("Duration")
                    myInstance.selectManifestData("MajorVersion")
                    myInstance.insertSmoothAttr("major_version",str(majorV),str(streamer),str(dateSup))
                    """
                    look = manifest.getAttribSmoothStreamingMedia("LookAheadFragmentCount")
                    myInstance.selectManifestData("LookAheadFragmentCount")
                    myInstance.insertSmoothAttr("look_ahead_fragment_count",str(look),str(streamer),str(dateSup))
                    
                    
                    """
                    print "----StreamIndex Video----"
                    Type = manifest.getStreamIndexAttribute("video","Type")
                    print Type
                    Name = manifest.getStreamIndexAttribute("video","Name")
                    print Name
                    NbrChunks = manifest.getStreamIndexAttribute("video","Chunks")
                    #print Chunks
                    QualityLevels = manifest.getStreamIndexAttribute("video","QualityLevels")
                    print QualityLevels
                    MaxWidth = manifest.getStreamIndexAttribute("video","MaxWidth")
                    print MaxWidth
                    MaxHeight = manifest.getStreamIndexAttribute("video","MaxHeight")
                    print MaxHeight
                    DisplayWidth = manifest.getStreamIndexAttribute("video","DisplayWidth")
                    print DisplayWidth
                    DisplayHeight = manifest.getStreamIndexAttribute("video","DisplayHeight")
                    print DisplayHeight
                    Url = manifest.getStreamIndexAttribute("video","Url")
                    print Url
                    print "-----QualityLevel Video-----"
                    
                    IndexVideo= manifest.getQualityLevelAttribute("video","Index")
                    """
                    
                    BitrateVideo= manifest.getQualityLevelAttribute("video","Bitrate")
                    print (BitrateVideo)
                    for bit in BitrateVideo:
                        print (bit)
                        myInstance.insertQltyAttr("bitrate","video",str(bit),str(streamer),str(dateSup))
                    
                    BitrateVideo= manifest.getQualityLevelAttribute("audio","Bitrate")
                    print (BitrateVideo)
                    for bit in BitrateVideo:
                        print (bit)
                        myInstance.insertQltyAttr("bitrate","audio",str(bit),str(streamer),str(dateSup))
                    
                    """
                    FourCCVideo= manifest.getQualityLevelAttribute("video","FourCC")
                    MaxWidthQuality= manifest.getQualityLevelAttribute("video","MaxWidth")
                    MaxHeightQuality= manifest.getQualityLevelAttribute("video","MaxHeight")
                    CodecPrivateDataVideo= manifest.getQualityLevelAttribute("video","CodecPrivateData")
                    
                    #liste = manifest.getChunksAttribute("video", "d")
                    #manifest.viewList(liste)
                    #print ":".join(liste)
                    
                    print "----StreamIndex Audio---"
                    TypeAudio = manifest.getStreamIndexAttribute("audio","Type")
                    print TypeAudio
                    IndexAudio = manifest.getStreamIndexAttribute("audio","Index")
                    print IndexAudio
                    LanguageAudio = manifest.getStreamIndexAttribute("audio","Language")
                    print LanguageAudio
                    NameAudio = manifest.getStreamIndexAttribute("audio","Name")
                    print "Name Audio "+ NameAudio
                    NbrChunksAudio = manifest.getStreamIndexAttribute("audio","Chunks")
                    print "Chunk Vidéo : "+ NbrChunks
                    print "Chunk Audio : "+ NbrChunksAudio
                    TestChunksVideo = manifest.getChunksAttribute("video","d")
                    TestChunksAudio = manifest.getChunksAttribute("audio","d")
                    QualityLevelsAudio = manifest.getStreamIndexAttribute("audio","QualityLevels")
                    print QualityLevelsAudio
                    UrlAudio = manifest.getStreamIndexAttribute("audio","Url")
                    print UrlAudio
                    print "-----QualityLevel Audio-----"
                    
                    BitrateAudio = manifest.getQualityLevelAttribute("audio","Bitrate")
                    FourCCAudio = manifest.getQualityLevelAttribute("audio","FourCC")
                    SamplingRateAudio = manifest.getQualityLevelAttribute("audio","SamplingRate")
                    ChannelsAudio= manifest.getQualityLevelAttribute("audio","Channels")
                    BitsPerSampleAudio= manifest.getQualityLevelAttribute("audio","BitsPerSample")
                    PacketSizeAudio = manifest.getQualityLevelAttribute("audio","PacketSize")
                    AudioTagAudio = manifest.getQualityLevelAttribute("audio","AudioTag")
                    CodecAudio = manifest.getQualityLevelAttribute("audio","CodecPrivateData")
                    #MaxHeightAudio=manifest.getQualityLevelAttribute("audio","CodecPrivateData")
                    #MaxWidthAudio= manifest.getQualityLevelAttribute("audio","CodecPrivateData")
                    #liste2 = manifest.getChunksAttribute("audio", "d")
                    #print ":".join(liste2)
                             
                    myInstance = BDD("192.168.134.122", "adama", "adama", "ABSTRACT")
                    myInstance.insertPod("Poda", "strm.poda.manager.cdvr.orange.fr", "Description du Poda")
                    myInstance.insertPod("Podb", "strm.podb.manager.cdvr.orange.fr", "Description du Podb")               
                    theFile = open(element, 'rb').read()
                    #myInstance.insertSmoothMedia(0,NameSmooth, MajorVersion, MinorVersion, Duration, DVRWindowLength, LookAheadFragmentCount, IsLive, CanSeek, CanPause, '2016-11-01 09:24:28', '1', theFile,0, Type + ":"+TypeAudio, Name, NameAudio, NbrChunks, NbrChunksAudio, TestChunksVideo, TestChunksAudio, QualityLevels, QualityLevelsAudio, MaxWidth, MaxHeight, MaxWidthQuality, MaxHeightQuality, DisplayWidth, DisplayHeight, Url, UrlAudio, IndexAudio, LanguageAudio, IndexVideo, IndexAudio, BitrateVideo, BitrateAudio, FourCCVideo, FourCCAudio, CodecPrivateDataVideo, CodecAudio, SamplingRateAudio, ChannelsAudio, BitsPerSampleAudio, PacketSizeAudio, AudioTagAudio)
                   """
                    """
                     (`id`, `name_smooth`, `major_version`, `minor_version`, `duration`, `dvr_window_length`, `look_ahead_fragment_count`, `is_live`, `can_seek`, `can_pause`, `date_manifest`, `smooth_ok`, `manifest_file`, `manifest_file_content_type`, `type_stream_index`, `name_video`, `name_audio`, `nbr_chunks_video`, `nbr_chunks_audio`, `chunks_video`, `chunks_audio`, `quality_levels_video`, 
                     `quality_levels_audio`, `max_width_video`, `max_height_video`, `max_width_audio`, `max_height_audio`, `display_width_video`, `display_height_video`, `url_video`, `url_audio`, `index_strm_audio`, `language`, `index_qlity_video`, `index_qlity_audio`, `bitrate_video`, `bitrate_audio`, `four_cc_video`, `four_cc_audio`, `codec_private_data_video`, `codec_private_data_audio`, `sampling_rate`, `channels`, `bits_per_sample`, `packet_size`, `audio_tag`) 
                     
                    """  
                    #manifest.viewList(liste2)
                    """
                    date_manifest
                    smooth_ok
                    manifest_file
                    manifest_file_content_type
                    type
                    name
                    chunks_video
                    quality_levels_video
                    max_width
                    max_height
                    display_width
                    display_height
                    url
                    language
                    chunks_audio
                    quality_levels_audio
                    index_qlity
                    bitrate
                    four_cc
                    codec_private_data
                    sampling_rate
                    channels
                    bits_per_sample
                    packet_size
                    audio_tag
                    
                    """
                
                myInstance.commitTransax()
                myInstance.closeConnection() 
            
            time.sleep(5)
            print ("\n-------------LIVE---------------\n")
            print ("\nSMOOTH\n")
            mss = routeMSS.getManifest("LIVE", "smooth")
            routeMSS.download(mss)
            time.sleep(5)
            routeDASH = Route()
            print ("\nDASH\n")
            dash = routeDASH.getManifest("LIVE", "dash")
            routeDASH.download(dash)
            time.sleep(5)
            routeHLS = Route()
            print ("\nHLS\n")
            hls = routeHLS.getManifest("LIVE", "hls")
            routeHLS.download(hls)
            time.sleep(5)
            print ("\n-------------END LIVE---------------\n")
            
            i = i +1
