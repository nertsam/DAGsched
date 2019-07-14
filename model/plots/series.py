import plot_design
from matplotlib.backends.backend_pdf import PdfPages
from os import listdir
from os.path import isfile, join


experiment01 = plot_design.plot([['SOF-DWM-8-20-100.npy', 'SOF-DBM-8-20-100.npy', 'SOF-EBE-8-20-100.npy', 'SOF-EBM-8-20-100.npy', 'S-FED-8-20-100.npy'],['SOF-DWM-16-20-100.npy', 'SOF-DBM-16-20-100.npy', 'SOF-EBE-16-20-100.npy', 'SOF-EBM-16-20-100.npy', 'S-FED-16-20-100.npy'],['SOF-DWM-32-20-100.npy', 'SOF-DBM-32-20-100.npy', 'SOF-EBE-32-20-100.npy', 'SOF-EBM-32-20-100.npy', 'S-FED-32-20-100.npy']])
save_pdf = PdfPages('constrained.pdf')
save_pdf.savefig(experiment01, bbox_inches='tight', pad_inches=0.0)
save_pdf.close()

"""
experiment01 = plots.plot('', 'S-FED-8-20-100.npy', 'SOF-DWE-8-20-100.npy', 'SOF-EFM-8-20-100.npy', 'SOF-DBE-8-20-100.npy',
'SOF-DWM-8-20-100.npy', 'SOF-EWE-8-20-100.npy', 'SOF-DBM-8-20-100.npy', 'SOF-EBE-8-20-100.npy', 'SOF-EWM-8-20-100.npy',
'SOF-DFE-8-20-100.npy', 'SOF-EBM-8-20-100.npy', 'SOF-DFM-8-20-100.npy', 'SOF-EFE-8-20-100.npy')

save_pdf = PdfPages('test01_8_constrained.pdf')
save_pdf.savefig(experiment01)
save_pdf.close()


experiment02 = plots.plot('', 'S-FED-16-20-100.npy', 'SOF-DWE-16-20-100.npy', 'SOF-EFM-16-20-100.npy', 'SOF-DBE-16-20-100.npy',
'SOF-DWM-16-20-100.npy', 'SOF-EWE-16-20-100.npy', 'SOF-DBM-16-20-100.npy', 'SOF-EBE-16-20-100.npy', 'SOF-EWM-16-20-100.npy',
'SOF-DFE-16-20-100.npy', 'SOF-EBM-16-20-100.npy', 'SOF-DFM-16-20-100.npy', 'SOF-EFE-16-20-100.npy')

save_pdf = PdfPages('test01_16_constrained.pdf')
save_pdf.savefig(experiment02)
save_pdf.close()

experiment03 = plots.plot('', 'S-FED-32-20-100.npy', 'SOF-DWE-32-20-100.npy', 'SOF-EFM-32-20-100.npy', 'SOF-DBE-32-20-100.npy',
'SOF-DWM-32-20-100.npy', 'SOF-EWE-32-20-100.npy', 'SOF-DBM-32-20-100.npy', 'SOF-EBE-32-20-100.npy', 'SOF-EWM-32-20-100.npy',
'SOF-DFE-32-20-100.npy', 'SOF-EBM-32-20-100.npy', 'SOF-DFM-32-20-100.npy', 'SOF-EFE-32-20-100.npy')

save_pdf = PdfPages('test01_32_constrained.pdf')
save_pdf.savefig(experiment03)
save_pdf.close()
"""
