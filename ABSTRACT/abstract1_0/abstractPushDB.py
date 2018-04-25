#!/usr/bin/python
#-*- coding: utf-8 -*-

from route.Route import *
from database.BDD import *
from validation.Validation import *
from recup.dataManifest import *
if __name__ == "__main__":
    routeMSS = Route()
    print "------ DATABASE--------" 
    listNamePods = routeMSS.getPods()
    listLinkPods = routeMSS.getAllLinksPods()
    print listNamePods
    print listLinkPods
    chaine = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s"
    chaine2 = "0,'2', '3', '4', '5', '6', '7', '1', '1', '1', '2016-11-01 09:24:28', '1', 0, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46'"
    chaineParam = "param[0],param[1],param[2],param[3],param[4],param[5],param[6],param[7],param[8],param[9],param[10],param[11],param[12],param[13],param[14],param[15],param[16],param[17],param[18],param[19],param[20],param[21],param[22],param[23],param[24],param[25],param[26],param[27],param[28],param[30],param[31],param[32],param[33],param[34],param[35],param[36],param[37],param[38],param[39],param[40],param[41],param[42],param[43],param[44],param[45]"
    liste = chaine.split(",")
    liste2 = chaine2.split(",")
    liste3 = chaineParam.split(",")
    print len(liste)
    print len(liste2)
    print len(liste3)
    myInstance = BDD("192.168.134.122","adama", "adama", "ABSTRACT")
    myInstance.insertPod("Poda", "strm.poda.manager.cdvr.orange.fr", "Description du Poda")
    myInstance.insertPod("Podb", "strm.podb.manager.cdvr.orange.fr", "Description du Podb")
    theFile = open('Manifest.xml', 'rb').read()
    myInstance.insertSmoothMedia(0,'2', '3', '4', '5', '6', '7', '1', '1', '1', '2016-11-01 09:24:28', '1', theFile, '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46')
    """
     (`id`, `name_smooth`, `major_version`, `minor_version`, `duration`, `dvr_window_length`, `look_ahead_fragment_count`, `is_live`, `can_seek`, `can_pause`, `date_manifest`, `smooth_ok`, `manifest_file`, `manifest_file_content_type`, `type_stream_index`, `name_video`, `name_audio`, `nbr_chunks_video`, `nbr_chunks_audio`, `chunks_video`, `chunks_audio`, `quality_levels_video`, `quality_levels_audio`, `max_width_video`, `max_height_video`, `max_width_audio`, `max_height_audio`, `display_width_video`, `display_height_video`, `url_video`, `url_audio`, `index_strm_audio`, `language`, `index_qlity_video`, `index_qlity_audio`, `bitrate_video`, `bitrate_audio`, `four_cc_video`, `four_cc_audio`, `codec_private_data_video`, `codec_private_data_audio`, `sampling_rate`, `channels`, `bits_per_sample`, `packet_size`, `audio_tag`) 
     
    """
    myInstance.commitTransax()
    myInstance.closeConnection()    