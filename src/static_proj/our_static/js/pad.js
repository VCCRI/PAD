warningCount = 0;

if ((document.getElementById("id_peak_File") === null) === false) {
    document.getElementById("id_peak_File").onchange = function(){
        if (document.getElementById("id_peak_File").files.length > 0 && warningCount == 0){
            alert('Warning! Uploading custom file(s) will result in a longer processing time.');
            warningCount += 1;
        };
    };
};

if ((document.getElementById("id_new_peak_File") === null) === false) {
    document.getElementById("id_new_peak_File").onchange = function(){
        if (document.getElementById("id_new_peak_File").files.length > 0 && warningCount == 0){
            alert('Warning! Uploading custom file(s) will result in a longer processing time.');
            warningCount += 1;
        };
    };
};