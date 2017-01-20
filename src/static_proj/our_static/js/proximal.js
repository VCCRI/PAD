// plots proximal heatmap with dendrogram using Plotly.js

var i;
var trace = [];

// dendogram
if (json_data['proximal_dendrogram'] != "None") {
    var proximal_dendrogram = json_data['proximal_dendrogram'];

    for (i = 0;  i < proximal_dendrogram['dcoord'].length; i++){
        var t = {
            x: proximal_dendrogram['icoord'][i],
            y: proximal_dendrogram['dcoord'][i],
            marker: {color: "rgb(0,204,102)"},
            mode: "lines",
            type: "scatter",
            xaxis: "xs",
            yaxis: "y2"
        };
        trace.push(t);
    }
    for (i = 0;  i < proximal_dendrogram['dcoord'].length; i++){
        var t = {
            x: proximal_dendrogram['dcoord'][i],
            y: proximal_dendrogram['icoord'][i],
            marker: {color: "rgb(0,204,102)"},
            mode: "lines",
            type: "scatter",
            xaxis: "x2",
            yaxis: "ys"
        };
        trace.push(t);
    }
}

var m = [5.0];
var increment = 10.0;
for (i = 1; i < json_data['matrix_size']; i++) {
    m.push(m[i-1] + increment)
}

var proximal_fc_limit = json_data['proxdist_fc_limit'][0];

// heatmap
var trace00 = [
    {
        z: json_data['proximal_matrix'],
        x: m,
        y: m,
        text: json_data['proximal_pval_matrix'],
        type: 'heatmap',
        zmin: proximal_fc_limit[0],
        zmax: proximal_fc_limit[-1],
        hoverinfo: 'x+y+z+text',
    }
];

var prox_layout = {
    autosize: true,
    bargap: 0,
    height: document.getElementById('heatmap').offsetWidth - 150,
    hovermode: "closest",
    showlegend: false,
    width: document.getElementById('heatmap').offsetWidth,
    margin: {
        l: 150,
        r: 50,
        b: 150,
        t: 50,
        pad: 2
    },
    xaxis: {
        autotick: false,
        domain: [0.1, 0.85],
        dtick: 1,
        mirror: "allticks",
        rangemode: "tozero",
        showgrid: false,
        showline: true,
        showticklabels: true,
        tickmode: "array",
        ticks: "inside",
        ticktext: json_data['p_filename'],
        tickvals: m,
        type: "linear",
        zeroline: false
    },
    xaxis2: {
        domain: [0.85, 1],
        showgrid: false,
        zeroline: false
    },
    yaxis: {
        autotick: false,
        domain: [0, 0.86],
        dtick: 1,
        mirror: "allticks",
        rangemode: "tozero",
        showgrid: false,
        showline: true,
        showticklabels: true,
        tickmode: "array",
        ticks: "inside",
        ticktext: json_data['p_filename'],
        tickangle: 0,
        tickvals: m,
        type: "linear",
        zeroline: false
    },
    yaxis2: {
        domain: [0.85, 1],
        showgrid: false,
        zeroline: false
    }
};

var prox_data = trace.concat(trace00);

// Plot
Plotly.newPlot('proximal', prox_data, prox_layout, {displaylogo: false});

console.log("Processing time: "+json_data['proc_time'])

// var svg = document.getElementById("proximal");

var svg = document.getElementById("proximal").getElementsByClassName("main-svg")

var output_svg = svg[0].cloneNode()

for (let svg_node of svg) {
    for (let child_node of svg_node.childNodes) {
        if (child_node.tagName == "g") {
            output_svg.appendChild(child_node.cloneNode(true))
        }
    }
}

var serializer = new XMLSerializer();

var source = serializer.serializeToString(output_svg);

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
document.getElementById("proximalSvg").href = url;
//you can download svg file by right click menu.
