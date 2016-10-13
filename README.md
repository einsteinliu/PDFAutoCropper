# PDFAutoCropper

A tool which can detect and crop the text from scanned pdf files of books. It handle the pdf pages as images and need GhostScript and ImageMagic to do the pdf->image, image->pdf conversion.

## Core Ideas

The core ideas of the text detection algorithm are:

1. Radon transform
2. Special intensity distribution of text image patches
3. The horizontal projection of the text block shows a special distribution(text is always arranged as lines), this can help us to correct the page orientation.
4. The text image patches can be used to form a training set for the future use.

## Cropper

The C++ version using opencv with GPU support.

## pdfCropStein

Python version as prototype

## Papers

Papers related to this task.