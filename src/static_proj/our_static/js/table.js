// javascript for peak selection from database table

$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = parseInt( $('#min').val(), 10 );
        var max = parseInt( $('#max').val(), 10 );
        var num_peaks = parseFloat( data[2] ) || 0; // use data for the peaks column

        if ( ( isNaN( min ) && isNaN( max ) ) ||
             ( isNaN( min ) && num_peaks <= max ) ||
             ( min <= num_peaks   && isNaN( max ) ) ||
             ( min <= num_peaks   && num_peaks <= max ) )
        {
            return true;
        }
        return false;
    }
);

$(document).ready(function() {
    // Setup - add a text input to each footer cell
    $('#table tfoot th').each( function () {
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" />' );
    } );

    $('#table').DataTable( {
        dom: 'T<"clear">lfrtip',
        tableTools: {
            "sRowSelect": "multi",
            "aButtons": [ "select_all", "select_none" ]
        },
        "lengthMenu": [[10, 25, 50, 100, 200, -1], [10, 25, 50, 100, 200, "All"]],
    } );

    // DataTable
    var table = $('#table').DataTable();

    // Apply the search
    table.columns().every( function () {
        var that = this;

        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );

    $('#min, #max').keyup( function() {
        table.draw();
    } );

} );

// when save button is clicked, display the files selected in forms.
saveRows = function(){
    var rowArray = $('.selected');
    // alert(rowArray[0].id)
    var filename = '';
    for (var i = 0; i < rowArray.length; i++) {
        filename = filename.concat(rowArray[i].id);
        filename = filename.concat('\n');
    }
    $('#id_selected_peaks').text(filename);

};
