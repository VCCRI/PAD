// javascript for peak file selection table for plotting

$('#plot-select').ready(function() {

    $('#plot-table').DataTable( {
        dom: 'T<"clear">lfrtip',
        tableTools: {
            "aButtons": []
        },
        "lengthMenu": [[5, 10, 15, 25, -1], [5, 10, 15, 25, "All"]],
    } );

    // DataTable
    var table = $('#plot-table').DataTable();

    // Apply the search
    table.columns().every( function () {
        var that = this;
        $( 'input', this.footer() ).on( 'click keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );

    $('#plot').modal({
        keyboard: true,
        backdrop: "static",
        show:false,
    });

    $("#submit-user-input").on('click', function () {
        if (document.getElementById('id_pvalue').checkValidity()) {
            // Enable overlay and spinner
            $('#overlay').show()
            $('.spinner').show()
            $(document.body).addClass('modal-open');
        }
    });
});
