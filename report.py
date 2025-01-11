from pptx import Presentation
from pptx.util import Inches
import os
import time
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def create_report(image_path, result, filename):
    # Create a PowerPoint presentation object
    prs = Presentation()

    # Add title slide
    slide_layout = prs.slide_layouts[0]  # 0 is the title slide layout
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "Plastic Detection Report"
    subtitle.text = f"Analysis for {filename}"

    # Add slide for image
    slide_layout = prs.slide_layouts[5]  # 5 is a blank slide layout
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.add_picture(image_path, Inches(0.5), Inches(1), height=Inches(4.5))

    # Add slide for analysis result
    slide = prs.slides.add_slide(prs.slide_layouts[1])  # 1 is the Title and Content layout
    title = slide.shapes.title
    title.text = "Analysis Result"

    content = slide.shapes.placeholders[1]
    content.text = result

    # Ensure the reports folder exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Create a unique filename for the report
    timestamp = int(time.time())
    report_filename = f"{timestamp}_{filename.split('.')[0]}_report.pptx"

    # Save the presentation to a file in the 'reports' folder
    report_path = os.path.join('reports', report_filename)
    prs.save(report_path)

    return report_path


# from fpdf import FPDF
# import os
# import time
# import cv2
# import warnings
# warnings.filterwarnings("ignore", category=FutureWarning)

# def create_report(image_path, result, filename):
#     # Load image using OpenCV for further processing (e.g., drawing bounding boxes)
#     image = cv2.imread(image_path)

#     # Create a PDF document
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # Add title to the report
#     pdf.set_font("Arial", size=16)
#     pdf.cell(200, 10, txt="Plastic Detection Report", ln=True, align="C")
#     pdf.cell(200, 10, txt=f"Analysis for {filename}", ln=True, align="C")

#     # Add image to the report (resize the image if necessary)
#     pdf.ln(10)
#     pdf.image(image_path, x=10, y=40, w=180)  # Adjust positioning and width as necessary

#     # Add analysis result for each detected object
#     pdf.ln(10)
#     pdf.set_font("Arial", size=12)
#     for obj in result['objects']:
#         label = obj.get('label', 'Unknown')
#         bbox = obj.get('bbox', [0, 0, 0, 0])
#         color = obj.get('color', 'Unknown')
#         importance = obj.get('importance', 'Normal')

#         # Add object details to the report
#         pdf.cell(200, 10, txt=f"Object: {label}", ln=True)
#         pdf.cell(200, 10, txt=f"Color: {color}", ln=True)
#         pdf.cell(200, 10, txt=f"Position: {bbox}", ln=True)
#         pdf.cell(200, 10, txt=f"Importance: {importance}", ln=True)
#         pdf.ln(5)  # Adding some space between objects

#     # Ensure the reports folder exists
#     if not os.path.exists('reports'):
#         os.makedirs('reports')

#     # Create a unique filename for the report
#     timestamp = int(time.time())
#     report_filename = f"{timestamp}_{filename.split('.')[0]}_report.pdf"

#     # Save the PDF to the 'reports' folder
#     report_path = os.path.join('reports', report_filename)
#     pdf.output(report_path)

#     return report_path
