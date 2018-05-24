var projection = ol.proj.get('EPSG:3857');

var dragBoxSubset = new ol.layer.Vector({
    source: new ol.source.Vector(),
    visible: true,
    title: 'subset',
    projection: projection,
    style: [new ol.style.Style({
    	fill: new ol.style.Fill({
    	    color: 'rgba(255,204,204,0.3)'
    	}),
    	stroke: new ol.style.Stroke({
    	    color: 'rgba(255,153,153,1)', 
    	    width: 2
    	})
    })]
});

var etopo1 = new ol.layer.Tile({
    extent: [-20026376.39,-20048966.10,20026376.39,20048966.10],
    source: new ol.source.TileWMS({
        url: 'https://www.ngdc.noaa.gov/thredds/wms/global/ETOPO1_Ice_g_gmt4.nc',
	parmas: {'LAYERS': 'z','service': 'WMS', 'version': '1.3.0', 'request': 'GetMap', 'coverage': 'z', 'format': 'image/png', 'crs': 'EPSG:4326', 'styles': 'boxfill/alg', 'elevation': '0', 'colorscalerange': '-5000,5000', 'logscale': 'false', 'exceptions': 'XML', 'numcolorbands': '20', 'transparent': 'True'},
	ratio: 1,
	projection: projection
    })
});

var sat = new ol.layer.Tile({
    title: 'sat',
    source: new ol.source.OSM ({
	layer: 'sat'
    }),
});

var regional = new ol.layer.Vector({
    visible: true,
    title: 'Regional',
    projection: projection,
    source: new ol.source.Vector({
	attributions: [
            '<a href="https://www.ngdc.noaa.gov/thredds/catalog/regional/catalog.html">Regional Digital Elevation Models</a>',
            ol.source.OSM.ATTRIBUTION
        ],
        url: 'data/kml/thredds_regional.kml',
        format: new ol.format.KML({extractStyles: false})
    }),
    style: [new ol.style.Style({
    	fill: new ol.style.Fill({
    	    color: 'rgba(204,255,204,0.3)'
    	}),
    	stroke: new ol.style.Stroke({
    	    color: 'rgba(0,0,0,0.7)', 
    	    width: 1
    	})
    })]
});

var crm = new ol.layer.Vector({
    visible: false,
    title: 'CRM',
    projection: projection,
    source: new ol.source.Vector({
	attributions: [
            '<a href="https://www.ngdc.noaa.gov/thredds/catalog/regional/CRM/catalog.html"> Integrated Models of Coastal Relief</a>',
            ol.source.OSM.ATTRIBUTION
        ],
        url: 'data/kml/thredds_CRM.kml',
        format: new ol.format.KML({extractStyles: false})
    }),
    style: [ new ol.style.Style({
    	fill: new ol.style.Fill({
    	    color: 'rgba(255,102,178,0.3)'
    	}),
    	stroke: new ol.style.Stroke({
    	    color: 'rgba(0,0,0,0.7)', 
    	    width: 1
    	})
    })]
});

var pmel = new ol.layer.Vector({
    visible: false,
    title: 'PMEL',
    projection: projection,
    source: new ol.source.Vector({
	attributions: [
            '<a href="http://nctr.pmel.noaa.gov/">PMEL</a> <a href="https://www.ngdc.noaa.gov/thredds/catalog/pmel/catalog.html">Forecast Grids for MOST Model</a>',
            ol.source.OSM.ATTRIBUTION
        ],
        url: 'data/kml/thredds_pmel.kml',
        format: new ol.format.KML({extractStyles: false})
    }),
    style: [ new ol.style.Style({
    	fill: new ol.style.Fill({
    	    color: 'rgba(255,204,153,0.3)'
    	}),
    	stroke: new ol.style.Stroke({
    	    color: 'rgba(0,0,0,0.7)', 
    	    width: 1
    	})
    })]
});

var global = new ol.layer.Vector({
    visible: false,
    title: 'Global',
    projection: projection,
    source: new ol.source.Vector({
	attributions: [
            '<a href="https://www.ngdc.noaa.gov/thredds/catalog/global/catalog.html">Global Digital Elevation Models</a>',
            ol.source.OSM.ATTRIBUTION
        ],
        url: 'data/kml/thredds_global.kml',
        format: new ol.format.KML({extractStyles: false})
    }),
    style: [ new ol.style.Style({
    	fill: new ol.style.Fill({
    	    color: 'rgba(255,229,204,0.1)'
    	}),
    	stroke: new ol.style.Stroke({
    	    color: 'rgba(0,0,0,0.7)', 
    	    width: 1
    	})
    })]
});

var demTiles = new ol.layer.Vector({
    visible: false,
    title: 'DEM Tiles',
    projection: projection,
    source: new ol.source.Vector({
	attributions: [
            '<a href="https://www.ngdc.noaa.gov/thredds/catalog/tiles/catalog.html">Ocean and Coastal Elevation Data for the U.S. Coast</a> ',
            ol.source.OSM.ATTRIBUTION
        ],
        url: 'data/kml/thredds_tiled_19as.kml',
        format: new ol.format.KML({extractStyles: false})
    }),
    style: (function() {
	var Style13 = [new ol.style.Style({
	    fill: new ol.style.Fill({
		color: 'rgba(160,155,100,0.3)'
	    }),
	    stroke: new ol.style.Stroke({
		color: 'rgba(0,0,0,0.7)',
		width: 1
	    })
	})];
	var Style19 = [new ol.style.Style({
		      fill: new ol.style.Fill({
			  opacity: 0.6,
			  color: 'rgba(119,146,179,0.3)'
		      }),
	    stroke: new ol.style.Stroke({
		color: 'rgba(0,0,0,0.7)',
		width: 1})
	})];
	var Style1 = [new ol.style.Style({
	    fill: new ol.style.Fill({
		opacity: 0.6,
		color: 'rgba(254,232,240,0.3)'
	    }),
	    stroke: new ol.style.Stroke({
		color: 'rgba(0,0,0,0.7)',
		width: 1})
	})];
	var Style3 = [new ol.style.Style({
		      fill: new ol.style.Fill({
			  opacity: 0.6,
			  color: 'rgba(254,249,175,0.3)'
		      }),
	    stroke: new ol.style.Stroke({
		color: 'rgba(0,0,0,0.7)',
		width: 1})
	})];
	return function(feature, resolution) {
	    if (feature.get('Resolution') == 19) {
		return Style19;
	    } else if (feature.get('Resolution') == 13) {
		return Style13;
	    } else if (feature.get('Resolution') == 1) {
		return Style1;
	    } else if (feature.get('Resolution') == 3) {
		return Style3;
	    } else {
		return Style13;
	    }
	};
    })()
});

//-- Map View --//

var map = new ol.Map({
    layers: [ sat, dragBoxSubset, regional, crm, pmel, global, demTiles ],
    target: 'map',
    controls: ol.control.defaults({
	attribution: false
    }),
    view: new ol.View({
	projection: projection,
	center: ol.proj.transform([-120, 32], 'EPSG:4326', 'EPSG:3857'),
	extent: ol.proj.transformExtent([-180,-90,180,90], 'EPSG:4326', 'EPSG:3857'),
	zoom: 3
    })
});

var infoBox = document.getElementById('info');
var coordsBox = document.getElementById('coords');

// ----------------------- //
// -- Feature Selection -- //
// ----------------------- //
var allLayers = map.getLayers().getArray();

var select = new ol.interaction.Select({
    condition: ol.events.condition.click,
    multi: true,
    layers: [ regional, crm, pmel, global, demTiles ],
    style: [ new ol.style.Style({
    	fill: new ol.style.Fill({
    	    color: 'rgba(153,153,255,0.3)'
    	}),
    	stroke: new ol.style.Stroke({
    	    color: 'rgba(0,0,255,0.5)', 
    	    width: 2
    	})
    })]
});

map.addInteraction(select);

var selectedFeatures = select.getFeatures();

var boxExtent = null;
var wgsExtent = null;

// a DragBox interaction used to select features by drawing boxes
var dragBox = new ol.interaction.DragBox({
    condition: ol.events.condition.platformModifierKeyOnly
});

map.addInteraction(dragBox);

var displayBoxSubset = function (boxExtent) {
    var boxFeature = new ol.Feature({
	geometry: new ol.geom.Polygon.fromExtent(boxExtent),
	name: 'My Polygon'
    });
    dragBoxSubset.getSource().addFeature(boxFeature);
    dragBoxSubset.setZIndex(999);
    map.getView().fit(boxFeature.getGeometry(), map.getSize())
}

dragBox.on('boxend', function() {
    // features that intersect the box are added to the collection of
    // selected features
    boxExtent = dragBox.getGeometry().getExtent();
    allLayers.forEach(function(layer) {
	if (layer.get('title') != 'sat' && layer.getVisible() == true) {
	    var vectorSource = layer.getSource();
	    vectorSource.forEachFeatureIntersectingExtent(boxExtent, function(feature) {
		selectedFeatures.push(feature);
	    });
	}
    });
    displayBoxSubset(boxExtent);
});

// clear selection when drawing a new box and when clicking on the map
dragBox.on('boxstart', function() {
    selectedFeatures.clear();
    dragBoxSubset.getSource().clear();
});

function clearSelected(){
    selectedFeatures.clear();
    dragBoxSubset.getSource().clear();
}

function isOdd(num) { return num % 2;}

selectedFeatures.on(['add', 'remove'], function() {
    dragBoxSubset.getSource().clear();
    var dlink = "dataLink";
    var names = selectedFeatures.getArray().map(function(feature) {
        return feature.get('name');
    });
    var titles = selectedFeatures.getArray().map(function(feature) {
        return feature.get('Title');
    });
    var data = selectedFeatures.getArray().map(function(feature) {
        return feature.get('Data');
    });
    var ncData = selectedFeatures.getArray().map(function(feature) {
        return feature.get('NC');
    });
    var metaData = selectedFeatures.getArray().map(function(feature) {
        return feature.get('Metadata');
    });
    var NCML = selectedFeatures.getArray().map(function(feature) {
        return feature.get('NCML');
    });
    var wcsUrl = selectedFeatures.getArray().map(function(feature) {
        return feature.get('WCS');
    });
    var zvar = selectedFeatures.getArray().map(function(feature) {
        return feature.get('zvar');
    });
    
    if (names.length > 0) {
	var output = '<strong>Data Access:</strong> <small> <a class="menuLinks" id="clearSel" title="Clear Selected Features" onclick=\'clearSelected(); \'>Clear Selection</a> | <a class="menuLinks" id="zoomSel" title="Zoom to Selected Features" onclick="zoomToSelected(\''+names[i]+'\')">Zoom to Seleced</a></small><hr />';
	for (var i = 0, ii = names.length; i<ii; i++){
	    output += '<div id="'+names[i]+'" style="padding: 20px 0 20px 0; z-index: 20;" onclick="zoomToFeature(\'' + names[i] + '\')" onmouseover="test(\''+names[i]+'\')" onmouseout="test1(\''+names[i]+'\')"><a title="DEM Data & Details" href=' + data[i] + '>' + titles[i] +  '</a><br /><small><i>'+names[i]+'.nc</i></small><br /><br />Data: <a title="Download NetCDF" href =' + ncData[i] + '>NetCDF</a>';
	    if (boxExtent != null) {
		wgsExtent = ol.proj.transformExtent(boxExtent, 'EPSG:3857', 'EPSG:4326');
		output += ' | <a title="Subset Boundary: '+wgsExtent[0].toFixed(4)+", "+wgsExtent[1].toFixed(4)+", "+wgsExtent[2].toFixed(4)+", "+wgsExtent[3].toFixed(4)+'" href="'+ wcsUrl[i] + '?service=WCS&version=1.0.0&request=GetCoverage&coverage='+ zvar[i] + '&bbox=' + wgsExtent[0] + ',' + wgsExtent[1] + ',' + wgsExtent[2] + ',' + wgsExtent[3] + '&format=NetCDF3">Subset</a><br />Metadata: <a title="DEM Metadata" href =' + metaData[i] + '>ISO</a> | <a title="DEM NCML Metadata" href=' + NCML[i] + '>NCML</a> | <a title="Download KML Boundary" href="/map/data/kml">KML</a></div><hr />';
	    } else {
		output += '<br />Metadata: <a title="DEM Metadata" href =' + metaData[i] + '>ISO</a> | <a title="DEM NCML Metadata" href=' + NCML[i] + '>NCML</a> | <a title="Download KML Boundary" href="/map/data/kml">KML</a></div><hr />';
	    }
	}
	infoBox.innerHTML = output;
    } else {
	boxExtent = null;
	wgsExtent = null;
        infoBox.innerHTML = '<strong>Data Access:</strong> <a class="clearSel" id="clearSel"></a><div id="dataLink" onmouseover="test()" onmouseout="test1()"><br /><small><code>Click</code> Select DEM tiles on the map<br /><code>Shift+Click</code> Select/deselect multiple DEMs<br /><code>Ctrl+Drag</code> Select and subset DEMs</small></div><br /><hr /><br /><p align="justify"><small> NCEI builds and distributes high-resolution, coastal digital elevation models (DEMs) that integrate ocean bathymetry and land topography to support NOAA\'s mission to understand and predict changes in Earth\'s environment, and conserve and manage coastal and marine resources to meet our Nation\'s economic, social, and environmental needs.<br /></small></p>';
    }
});

function zoomToSelected(featureList) {
    var features = selectedFeatures.getArray();
    var extent = features[0].getGeometry().getExtent();
    features.forEach(function(feature){
	ol.extent.extend(extent,feature.getGeometry().getExtent());
    });
    map.getView().fit(extent, map.getSize());
}
	
function zoomToFeature(fName) {
    selectedFeatures.getArray().forEach(function(feature) {
	if (feature.get('name') == fName) {
	    map.getView().fit(feature.getGeometry(), map.getSize())
	}
    });
}

// -- Layer Switcher -- //

document.getElementById('select').onclick = function() {
    var selectValue = document.getElementById('select').value;
    allLayers.forEach(function(layer) {
	selectedFeatures.clear();
	if (layer.get('title') != 'sat' && layer.get('title') != 'subset') {
	    if (selectValue == 'All') {		
		layer.setVisible(true);
	    } else {
		if (layer.get('title') == selectValue) {
		    layer.setVisible(true);
		} else {
		    layer.setVisible(false);
		}
	    }
	}
    });
}

var highlightStyleCache = {};
var featureOverlay = new ol.layer.Vector({
    source: new ol.source.Vector(),
    map: map,
    style: function (feature, resolution) {
        var text = resolution * 100000 < 10 ? feature.get('text') : '';
        if (!highlightStyleCache[text]) {
            highlightStyleCache[text] = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#000066',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(182,182,182,0.6)'
                }),
                text: new ol.style.Text({
                    font: '12px Calibri,sans-serif',
                    text: text,
                    fill: new ol.style.Fill({
                        color: '#000'
                    }),
                    stroke: new ol.style.Stroke({
                        color: '#f00',
                        width: 3
                    })
                })
            });
        }
        return highlightStyleCache[text];
    }
});

var highlight;
var displayFeatureInfo = function (feature1) {
    if (feature1 !== highlight) {
        if (highlight) {
            featureOverlay.getSource().removeFeature(highlight);
        }
        if (feature1) {
            featureOverlay.getSource().addFeature(feature1);
        }
        highlight = feature1;
    }  
};

function test(fName) {
    selectedFeatures.getArray().forEach(function(feature) {
	if (feature.get('name') == fName) {
	    displayFeatureInfo(feature);
	}
	document.getElementById(fName).style.backgroundColor = "rgba(230, 230, 230, 0.8)";
    });
}

function test1(fName) {
    featureOverlay.getSource().removeFeature(highlight);
    document.getElementById(fName).style.backgroundColor = "rgba(240, 240, 240, 0.1)";
    highlight=null;
}

$(map.getViewport()).on('mousemove', function(evt) {
    var pixel = map.getEventPixel(evt.originalEvent);
    var coord = map.getCoordinateFromPixel(pixel);
    var wgsCoord = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
    coordsBox.innerHTML="&nbsp;Position: " + wgsCoord[0].toFixed(4) + "&deg; | " + wgsCoord[1].toFixed(4) + "&deg;";
});
