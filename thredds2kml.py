#!/usr/bin/env python2
#
### Description:
# 
# Generate KML files of ngdc thredds directories.
#
### Code:

import urllib2
import sys
from xml.dom import minidom
import pprint
import json
from osgeo import ogr

def create_polygon(coords):          
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for coord in coords:
        ring.AddPoint(coord[0], coord[1])

    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly.ExportToWkt()


def get_coords(url_dict):

    print url_dict['cat']
    f = urllib2.urlopen(url_dict['cat'])
    xmldoc = minidom.parseString(f.read())
    ds = xmldoc.getElementsByTagName("dataset")
    dem_data={}
    dem_dicts=[]
    all_coords=[]
    lv1_coords=[]
    lv2_coords=[]
    lv3_coords=[]
    for node in ds:
        ds_name = node.attributes["name"].value
        print(ds_name)
        ds_url="%s%s" %(url_dict['ncml'], ds_name)
        ## JSON DEM-LIST ##
        if ds_name != "Regional" and ds_name !="Coastal Relief Model by Volume" and ds_name !="PMEL" and ds_name != "Global" and ds_name != "tiled_3as" and ds_name != "tiled_1as" and ds_name != "tiled_13as" and ds_name != "tiled_19as" :
            ##print("%s%s" %(url_dict['nc'], ds_name))
            dems={}
            g = urllib2.urlopen(ds_url)
            xmldoc2 = minidom.parseString(g.read())
            #atts = xmldoc2.getElementsByTagName("ncml:attribute")
            #print(ds_name)
            # dems['DEMTitle'] = ds_name
            # dems['Status'] = "Complete"
            # dems['Link'] = "https://www.ngdc.noaa.gov/thredds/catalog/regional/catalog.html?dataset=regionalDatasetScan/%s" %(ds_name)
            # dems['Spatial'] = "Unknown"
            # dems['VDatum'] = "Unknown"
            # dems['Year'] = "Unknown"
            # dems['HDatum'] = "Unknown"
                    
            # for att in atts:
            #     if att.attributes["name"].value=="geospatial_lon_resolution":
            #         dems['Spatial'] = att.attributes["value"].value
            #     if att.attributes["name"].value=="geospatial_bounds_vertical_crs":
            #         dems['VDatum'] = att.attributes["value"].value
            #     if att.attributes["name"].value=="geospatial_bounds_crs":
            #         dems['HDatum'] = att.attributes["value"].value
            #     if att.attributes["name"].value=="date_issued":
            #         dems['Year'] = att.attributes["value"].value
                            
            # dem_dicts.append(dems)
            ds_title = None
            ## DEM KML ##
            ds_atts = xmldoc2.getElementsByTagName("ncml:attribute")
            for ds_att in ds_atts:
                if ds_att.attributes["name"].value == "title":
                    ds_title = ds_att.attributes["value"].value.title()
                    if ds_title == "Gdal Band Number 1":
                        ds_title = None

            if not ds_title:
                ds_title = ds_name[:-3].replace("_"," ").title()
                        
            if url_dict['name'] == 'CRM':
                vnum = ds_title[5:-4]
                if vnum == "1":
                    crmloc = "Northeast Atlantic"
                elif vnum == "2":
                    crmloc = "Southeast Atlantic"
                elif vnum == "3":
                    crmloc = "Florida and Eastern Gulf of Mexico"
                elif vnum == "4":
                    crmloc = "Central Gulf of Mexico"
                elif vnum == "5":
                    crmloc = "Western Gulf of Mexico"
                elif vnum == "6":
                    crmloc = "Southern California"
                elif vnum == "7":
                    crmloc = "Central Pacific"
                elif vnum == "8":
                    crmloc = "Northwest Pacific"
                elif vnum == "9":
                    crmloc = "Puerto Rico"
                elif vnum == "10":
                    crmloc = "Hawaii"
                    
                ds_title = "NCEI Coastal Relief Model Volume %s - %s" %(vnum, crmloc)
                
            if url_dict['name'] == 'global':
                ds_title = ds_title[:-10].replace("_", " ").title()

            if url_dict['name'] == 'tiled_19as':
                ds_title = ds_name
                split_title = ds_title[:-3].split("_")
                tyear = split_title[3][:-2]
                tver = split_title[3][5:]
                ds_title = "NCEI 1/9 arc-second Tiled DEM: %s %s (%s - Version %s)" %(split_title[1], split_title[2], tyear, tver)

            if url_dict['name'] == 'tiled_13as':
                ds_title = ds_name
                split_title = ds_title[:-3].split("_")
                tyear = split_title[3][:-2]
                tver = split_title[3][5:]
                ds_title = "NCEI 1/3 arc-second Tiled DEM: %s %s (%s - Version %s)" %(split_title[1], split_title[2], tyear, tver)

            if url_dict['name'] == 'tiled_1as':
                ds_title = ds_name
                split_title = ds_title[:-3].split("_")
                tyear = split_title[3][:-2]
                tver = split_title[3][5:]
                ds_title = "NCEI 1 arc-second Tiled DEM: %s %s (%s - Version %s)" %(split_title[1], split_title[2], tyear, tver)

            if url_dict['name'] == 'tiled_3as':
                ds_title = ds_name
                split_title = ds_title[:-3].split("_")
                tyear = split_title[3][:-2]
                tver = split_title[3][5:]
                ds_title = "NCEI 3 arc-second Tiled DEM: %s %s (%s - Version %s)" %(split_title[1], split_title[2], tyear, tver)

            varis = xmldoc2.getElementsByTagName("ncml:variable")
            
            for vari in varis:
                variVal = vari.attributes["name"].value
                if variVal == "z" or variVal == "bathy" or variVal == "Band1":
                    zvar = variVal

            groups = xmldoc2.getElementsByTagName("group")
            for group in groups:
                #print(group.attributes["name"].value)
                if group.attributes["name"].value == "CFMetadata":
                    bounds = group.getElementsByTagName("attribute")
                    if bounds:
                        #print(bounds)
                        wl=-9999
                        el=-9999
                        sl=-9999
                        nl=-9999
                        dem_res=-9999
                        for bound in bounds:
                            #print(bound.attributes["name"].value)
                            if bound.attributes["name"].value == "geospatial_lon_min":
                                wl = float(bound.attributes["value"].value)
                            if bound.attributes["name"].value == "geospatial_lon_max":
                                el = float(bound.attributes["value"].value)
                            if bound.attributes["name"].value == "geospatial_lat_min":
                                sl = float(bound.attributes["value"].value)
                            if bound.attributes["name"].value == "geospatial_lat_max":
                                nl = float(bound.attributes["value"].value)
                            if bound.attributes["name"].value == "geospatial_lon_resolution":
                                dem_res = float(bound.attributes["value"].value)

                    
                        #if dem_res > 0.0001 and dem_res != -9999:
                        #print(dem_res)
                        if wl > 180: wl = wl-360
                        if el > 180: el = el-360
                        # if wl == -180: wl = wl+.5
                        # if el == 180: el = el-.5
                        # if sl == -90: sl = sl+.5
                        # if nl == 90: nl = nl-.5
                        lv1_coords = [ds_name[:-3], ds_title, zvar, (wl, nl), (wl, sl), (el, sl), (el, nl), (wl, nl)]
                        #print lv1_coords
                        all_coords.append(lv1_coords)
                        #else:
                         #   lv2_coords = [ds_name, (wl, nl), (wl, sl), (el, sl), (el, nl), (wl, nl)]
                          #  all_coords.insert(0,lv2_coords)
                        # elif dem_res < 0.0006:
                        #     lv2_coords = [ds_name, (wl, nl), (wl, sl), (el, sl), (el, nl), (wl, nl)]
                        #     all_coords.append(lv1_coords)
                        # else:
                        #     lv3_coords = [ds_name, (wl, nl), (wl, sl), (el, sl), (el, nl), (wl, nl)]
                        #     all_coords.append(lv1_coords)
                            

            g.close()
        dem_data['data']=dem_dicts
        #for i in lv3_coords:
          #  all_coords.append(i)
        #for i in lv2_coords:
         #   all_coords.append(i)
        #for i in lv1_coords:
         #   all_coords.append(i)
         #all_coords.append(lv1_coords)
        
    f.close()
    #pprint.pprint(dem_data)
    #json_data = json.dumps(dem_data)
    #print(json_data)
    return all_coords

def make_shp(coords, url_dict, res):
    ## OGR STUFF ##
    driver = ogr.GetDriverByName('KML')
    ds = driver.CreateDataSource("thredds_%s.kml" %(url_dict['name']))
    layer = ds.CreateLayer("thredds_%s" %(url_dict['name']), None, ogr.wkbPolygon)
    
    layer.CreateField(ogr.FieldDefn('Name', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('Title', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    layer.CreateField(ogr.FieldDefn('Data', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    layer.CreateField(ogr.FieldDefn('NC', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    layer.CreateField(ogr.FieldDefn('Metadata', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    layer.CreateField(ogr.FieldDefn('NCML', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('WMS', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    layer.CreateField(ogr.FieldDefn('WCS', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('maxx', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('minx', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('maxy', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    layer.CreateField(ogr.FieldDefn('miny', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('Resolution', ogr.OFTString))
    defn = layer.GetLayerDefn()

    layer.CreateField(ogr.FieldDefn('zvar', ogr.OFTString))
    defn = layer.GetLayerDefn()
    
    #import coords
    #print all_coords
    for coord in coords:
        #print coord
        ds_name = coord[0]
        #print(ds_name)
        if coord[3][0] >= -180 and coord[3][0] <= 180:
            poly = create_polygon(coord[3:])
            #print(poly)
            # Create a new feature (attribute and geometry)
            #print('creating feature')
            feat = ogr.Feature( layer.GetLayerDefn())
            feat.SetField("Name", str(ds_name))
            feat.SetField("Title", str(coord[1]))
            feat.SetField("NC", str("%s%s.nc" %(url_dict['nc'], ds_name)))
            feat.SetField("Data", str("%s%s.nc" %(url_dict['data'], ds_name)))
            feat.SetField("Metadata", str("%s%s.nc" %(url_dict['meta'], ds_name)))
            feat.SetField("NCML", str("%s%s.nc" %(url_dict['ncml'], ds_name)))
            feat.SetField("WMS", str("%s%s.nc" %(url_dict['wms'], ds_name)))
            feat.SetField("WCS", str("%s%s.nc" %(url_dict['wcs'], ds_name)))
            feat.SetField("minx", str("%f" %(coord[3][0])))
            feat.SetField("maxx", str("%f" %(coord[5][0])))
            feat.SetField("miny", str("%f" %(coord[4][1])))
            feat.SetField("maxy", str("%f" %(coord[3][1])))
            feat.SetField("Resolution", str("%f" %(res)))
            feat.SetField("zvar", str("%s" %(coord[2])))
            #print('creating geom')
            geom = ogr.CreateGeometryFromWkt(poly)
            feat.SetGeometry(geom)
            layer.CreateFeature(feat)
            # Save and close everything
            feat = geom = None  # destroy these
    ds = layer = feat = geom = None

crm_urls = {
    'name' : "CRM",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/crm/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/crm/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/crm/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/crm/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/crm/catalog.html?dataset=crmDatasetScan/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/crm/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/crm/"
}

regional_urls = {
    'name' : "regional",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/regional/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/regional/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/regional/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/regional/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/regional/catalog.html?dataset=regionalDatasetScan/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/regional/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/regional/"
}

pmel_urls = {
    'name' : "pmel",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/pmel/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/pmel/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/pmel/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/pmel/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/pmel/catalog.html?dataset=pmelDatasetScan/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/pmel/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/pmel/"
}

global_urls = {
    'name' : "global",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/global/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/global/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/global/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/global/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/global/catalog.html?dataset=globalDatasetScan/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/global/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/global/"
}

tiled_3as_urls = {
    'name' : "tiled_3as",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_3as/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/tiles/tiled_3as/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/tiles/tiled_3as/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/tiles/tiled_3as/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_3as/catalog.html?dataset=tilesDatasetScan/tiled_3as/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/tiles/tiled_3as/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/tiles/tiled_3as/"
}

tiled_1as_urls = {
    'name' : "tiled_1as",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_1as/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/tiles/tiled_1as/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/tiles/tiled_1as/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/tiles/tiled_1as/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_1as/catalog.html?dataset=tilesDatasetScan/tiled_1as/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/tiles/tiled_1as/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/tiles/tiled_1as/"
}

tiled_13as_urls = {
    'name' : "tiled_13as",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_13as/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/tiles/tiled_13as/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/tiles/tiled_13as/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/tiles/tiled_13as/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_13as/catalog.html?dataset=tilesDatasetScan/tiled_13as/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/tiles/tiled_13as/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/tiles/tiled_13as/"
}

tiled_19as_urls = {
    'name' : "tiled_19as",
    'cat' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_19as/catalog.xml",
    'nc' : "https://www.ngdc.noaa.gov/thredds/fileServer/tiles/tiled_19as/",
    'meta' : "https://www.ngdc.noaa.gov/thredds/iso/tiles/tiled_19as/",
    'ncml' : "https://www.ngdc.noaa.gov/thredds/ncml/tiles/tiled_19as/",
    'data' : "https://www.ngdc.noaa.gov/thredds/catalog/tiles/tiled_19as/catalog.html?dataset=tilesDatasetScan/tiled_19as/",
    'wms' : "http://www.ngdc.noaa.gov/thredds/wms/tiles/tiled_19as/",
    'wcs' : "http://www.ngdc.noaa.gov/thredds/wcs/tiles/tiled_19as/"
}

print("+--
 regional
+--")
coords = get_coords(regional_urls)
make_shp(coords, regional_urls, 0)

print("+--
  crm
+--")
coords = get_coords(crm_urls)
make_shp(coords, crm_urls, 0)

print("+--
  global
+--")
coords = get_coords(global_urls)
make_shp(coords, global_urls, 0)

print("+--
  pmel
+--")
coords = get_coords(pmel_urls)
make_shp(coords, pmel_urls, 0)

print("+--
  tiles
+--")
## Tiles ##
coords = get_coords(tiled_3as_urls)
make_shp(coords, tiled_3as_urls, 3)

coords = get_coords(tiled_1as_urls)
make_shp(coords, tiled_1as_urls, 1)

coords = get_coords(tiled_13as_urls)
make_shp(coords, tiled_13as_urls, 13)

coords = get_coords(tiled_19as_urls)
make_shp(coords, tiled_19as_urls, 19)

### End
