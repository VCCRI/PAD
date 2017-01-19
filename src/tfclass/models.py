from __future__ import unicode_literals

from django.db import models


# information about peaks in a file
class Peaks_db(models.Model):
    """
    The Peaks_db class defines the meta-data of the peakfiles in the database.
    **protein** - name of the protein.
    **fileID** - a unique indentifier of the file.
    **origFile** - actual original file name 
    **num_peaks** - number of peaks in the file.
    **cells** - cell where the peakfile data is dervied from.
    **labs** - lab name where this peakfile is from.
    **year** - year this file was published.
    """
    protein = models.CharField(max_length=20)
    fileID = models.CharField(db_index=True, max_length=100) # A unique identifier of the file  
    origFile = models.CharField(db_index=True, max_length=50) # actual original file name 
    num_peaks = models.IntegerField()
    cells = models.CharField(max_length=50, null=True)
    labs = models.CharField(max_length=50, null=True)
    year = models.IntegerField(null=True)

    def __unicode__(self):
        return u'%s %s %s %d %s %s' % (self.protein, self.origFile, self.fileID, self.num_peaks, self.cells, self.labs)

    def __str__(self):
        return '%s %s %s %d %s %s' % (self.protein, self.origFile, self.fileID, self.num_peaks, self.cells, self.labs)


# information about peakfile in database
class Peaks_db_file(models.Model):
    """
    The Peaks_db_file class defines information of the pre-separated actual file in the database.
    **cutoff** - a threshold cutoff value the file is separated by.
    **filename** - actual name of the file it is stored as.
    **origFile** - name of the original file before separation.
    **fileID** - a unique indentifier of the file.
    **path** - a path where the file is stored.
    """
    cutoff = models.IntegerField()
    filename = models.CharField(db_index=True, max_length=50) # actual file name of the stored file
    origFile = models.CharField(db_index=True, max_length=50) # actual original file name 
    fileID = models.CharField(max_length=100) # A unique identifier of the file
    path = models.FilePathField(max_length=500)
    
    def __unicode__(self):
        return u'%s %d %s %s' % (self.fileID, self.cutoff, self.filename, self.path)

    def __str__(self):
        return '%s %d %s %s' % (self.fileID, self.cutoff, self.filename, self.path)


# Details about the gene database
class Genes_db(models.Model):
    """
    The Genes_db class defines all the gene information stored in the database.
    **gene_db_name** - name of the gene file it belongs to.
    **name** - name of the gene.
    **chromosome** - chromosome number of the gene.
    **strand** - gene strand.
    **start** - start site (5' end).
    **end** - end site (3' end).
    **tsSite** - transcription start site. (start if strand=='+', end otherwise).
    """
    gene_db_name = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    chromosome = models.CharField(db_index=True, max_length=5)
    strand = models.CharField(max_length=1)
    start = models.IntegerField()
    end = models.IntegerField()
    tsSite = models.IntegerField(db_index=True)

    def __unicode__(self):
        return u'%s %s %s %d %d %d' % (self.name, self.chromosome, self.strand, self.start, self.end, self.tsSite)
    
    def __str__(self):
        return '%s %s %s %d %d %d' % (self.name, self.chromosome, self.strand, self.start, self.end, self.tsSite)
