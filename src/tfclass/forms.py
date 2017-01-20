from django import forms
from django.conf import settings

from multiupload.fields import MultiFileField

from .function import checkPeakFile

import csv
import os


# Input form for submission (in home page)
class InputForm(forms.Form):
    """
    The InputForm class is an initial form for users submission.
    A number of fields are required from user to select and upload.
    **selected_peaks** - selected peaks from the datatables (peaks from database chosen for analysis).
    **gene_database** - name of a gene from database to be used for determining proximal and distal.
    **peak_File** - user's peak file upload field where it can be 1 or more files.
    **cut_off** - a threshold cut off to determine proximal and distal.
    **heatmap** - an option to generate heatmap axis ordering. 
            (
                Independent: proximal and distal each separately show clustering.
                Follow prioximal: distal will not cluster and distal heatmap axis ordering will follow proximal heatmap axis ordering.
                Follow distal: proximal will not cluster and proximal heatmap axis ordering will follow distal heatmap axis ordering.
            )
    """

    # selected peak files from datatables
    selected_peaks = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly','rows':6, 'cols':22, 'style':'resize:none;'}))

    path = os.path.join(settings.STATIC_ROOT, 'csv', 'genenames.csv')
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        genenames_list = map(tuple, reader)
    genenames_tuple = tuple(genenames_list)
    GENENAMES_CHOICES = genenames_tuple
    gene_database = forms.ChoiceField(choices=GENENAMES_CHOICES, required=True)

    # user input peak file
    peak_File = MultiFileField(min_num=0, required=False, label='Upload custom peak file', help_text='File must be in the form of <br /> chrNum\tstart\tend')

    # cutoff field
    path = os.path.join(settings.STATIC_ROOT, 'csv', 'cutoffs.csv')
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        cutoff_list = map(tuple, reader)
    cutoff_tuple = tuple(cutoff_list)
    CUTOFF_CHOICES = cutoff_tuple
    cut_off = forms.ChoiceField(choices=CUTOFF_CHOICES, required=True, help_text='Threshold to separate proximal and distal elements')

    # plot choices
    PLOT_CHOICES = ( 
        ('Independent', 'Independent'),
        ('Follow proximal', 'Follow proximal'),
        ('Follow distal', 'Follow distal')
    )
    heatmap = forms.ChoiceField(choices=PLOT_CHOICES, required=True, label='Heatmaps clustering', help_text='Option to cluster the proximal and distal heatmaps independently or based on one of the heatmap')

    pvalue = forms.FloatField(label="P-Value cut off", max_value=1, min_value=0)

    #validating input
    def clean(self):
        cleaned_data = super(InputForm, self).clean()
        peak_File = cleaned_data.get('peak_File')
        if (peak_File is not None) and (not checkPeakFile(peak_File)):
            raise forms.ValidationError({'peak_File': ["Invalid file format.",]})        


# Input form for submission from results page
class VariableInputForm(forms.Form):
    """
    The VariableInputForm class is a form for users re-submission.
    A number of fields are required from user to select or upload.
    **selected_peaks** - selected peaks from the datatables (peaks from database chosen for analysis).
    **new_peak_File** - (optional) user's peak file upload field where it can be 1 or more files.
    **cut_off** - a threshold cut off to determine proximal and distal.
    **heatmap** - an option to generate heatmap axis ordering. 
            (
                Independent: proximal and distal each separately show clustering.
                Follow prioximal: distal will not cluster and distal heatmap axis ordering will follow proximal heatmap axis ordering.
                Follow distal: proximal will not cluster and proximal heatmap axis ordering will follow distal heatmap axis ordering.
            )
    """
    selected_peaks = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly','rows':6, 'cols':22, 'style':'resize:none;'}))

    # uploaded peak files from user
    USERPEAK_CHOICES = ()
    uploaded_peak_File = forms.MultipleChoiceField(choices=USERPEAK_CHOICES, required=False)
    new_peak_File = MultiFileField(min_num=0, required=False, label='Upload custom peak file', help_text='File must be in the form of <br /> chrNum\tstart\tend')

    path = os.path.join(settings.STATIC_ROOT, 'csv', 'cutoffs.csv')
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        cutoff_list = map(tuple, reader)
    cutoff_tuple = tuple(cutoff_list)
    CUTOFF_CHOICES = cutoff_tuple
    cut_off = forms.ChoiceField(choices=CUTOFF_CHOICES, required=True, help_text='Threshold to separate proximal and distal elements')

    PLOT_CHOICES = ( 
        ('Independent', 'Independent'),
        ('Follow proximal', 'Follow proximal'),
        ('Follow distal', 'Follow distal')
    )
    heatmap = forms.ChoiceField(choices=PLOT_CHOICES, required=True, label='Heatmaps clustering', help_text='Option to cluster the proximal and distal heatmaps independently or based on one of the heatmap')

    pvalue = forms.FloatField(label="P-Value cut off", max_value=1, min_value=0)
    # # validating input
    # def clean(self):
    #     cleaned_data = super(VariableInputForm, self).clean()
    #     uploaded_peak_File = cleaned_data.get('uploaded_peak_File')
    #     new_peak_File = cleaned_data.get('new_peak_File')
    #     if not uploaded_peak_File and not new_peak_File:
    #         raise forms.ValidationError({'uploaded_peak_File': ["",],
    #                                      'new_peak_File': ["At least one of these fields must be given",]})
    #     if not checkPeakFile(new_peak_File):
    #         raise forms.ValidationError({'new_peak_File': ["Invalid file format.",]})


