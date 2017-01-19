// plots scatter plot of peak of interest using Plotly.js

$('#plot').ready(function() {
    $("#plot").on('show.bs.modal', function(event){
        rowID = $(event.relatedTarget).data("id");
        var p_names = json_data['p_filename'];
        var d_names = json_data['d_filename'];
        var p_matrix = json_data['proximal_matrix'];
        var d_matrix = json_data['distal_matrix'];
        var d_values = [];
        var p_values = [];
        for (var i = 0; i < p_names.length; i++) {
            if (i != p_names.indexOf(rowID)) {
                d_values[i] = d_matrix[d_names.indexOf(rowID)][d_names.indexOf(p_names[i])];
                p_values[i] = p_matrix[p_names.indexOf(rowID)][p_names.indexOf(p_names[i])];
            }
        }

        var trace1 = {
            x: p_values,
            y: d_values,
            mode: 'markers',
            type: 'scatter',
            name: 'Team A',
            text: p_names,
            marker: { size: 12 }
        };

        var data = [ trace1 ];

        var layout = {
            xaxis: {
                title: 'Proximal jaccard values'
            },
            yaxis: {
                title: 'Distal jaccard values'
            },
            title:rowID
        };

        var config = {
            displaylogo: false,
            scrollZoom: true
        };

        Plotly.newPlot('myDiv', data, layout, config);

        var svg = document.getElementById("myDiv");

        var serializer = new XMLSerializer();

        var source = serializer.serializeToString(svg);

        //add name spaces.
        if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)){
            source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
        }
        if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)){
            source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
        }

        //add xml declaration
        source = '<?xml version="1.0" standalone="no"?>\r\n' + source;

        //convert svg source to URI data scheme.
        var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);
        //set url value to a element's href attribute.
        document.getElementById("scatterPlot").href = url;
        //you can download svg file by right click menu.
    });
});
