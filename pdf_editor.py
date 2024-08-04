from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
import random
import os


# Path to the PDF file (update this path as needed)
pdf_path = r""

# Path to the folder where edited PDFs will be saved
output_folder = r""

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

def create_watermark_pdf(text, watermark_path):
    c = canvas.Canvas(watermark_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 40)
    # Set color with 30% opacity
    c.setFillColor(Color(0.5, 0.5, 0.5, alpha=0.3))  # Gray color with 30% opacity

    # Calculate text width and height to center the text
    text_width = c.stringWidth(text, "Helvetica", 40)
    text_height = 40  # Approximate text height

    # Position the text in the center of the page
    x = (width - text_width) / 2
    y = (height - text_height) / 2

    c.drawString(x, y, text)
    c.save()

def pdf_operation(num):
    try:
        pdf_reader = PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        original_name = os.path.splitext(os.path.basename(pdf_path))[0]  # Get the original file name without extension

        if num == 2:
            # Reverse the pages
            writer = PdfWriter()
            for i in reversed(range(total_pages)):
                writer.add_page(pdf_reader.pages[i])
            filename = f"{original_name}_reversed_{random.randint(1, 100)}.pdf"
            output = os.path.join(output_folder, filename)
            with open(output, 'wb') as f:
                writer.write(f)
            print(f"Reversed PDF saved as {filename}")

        elif num == 1:
            # Delete pages
            print("Enter the page numbers or ranges to delete (e.g., 1,2,4-6):")
            pages_input = input("Pages to delete: ")
            pages_to_delete = set()
            min_page = float('inf')
            max_page = -1

            for part in pages_input.split(','):
                if '-' in part:
                    start, end = part.split('-')
                    try:
                        start, end = int(start), int(end)
                        if start <= end and start >= 1:
                            pages_to_delete.update(range(start - 1, end))  # Convert to 0-based index
                            min_page = min(min_page, start)
                            max_page = max(max_page, end)
                        else:
                            print(f"Invalid range: {part}")
                    except ValueError:
                        print(f"Invalid range format: {part}")
                else:
                    try:
                        page_number = int(part)
                        if page_number >= 1:
                            pages_to_delete.add(page_number - 1)  # Convert to 0-based index
                            min_page = min(min_page, page_number)
                            max_page = max(max_page, page_number)
                        else:
                            print(f"Invalid page number: {part}")
                    except ValueError:
                        print(f"Invalid page number format: {part}")

            pages_to_delete = sorted(pages_to_delete)
            writer = PdfWriter()
            for i in range(total_pages):
                if i not in pages_to_delete:
                    writer.add_page(pdf_reader.pages[i])

            if writer.pages:
                remaining_pages_start = max(max_page + 1, 1)
                remaining_pages_end = total_pages
            else:
                remaining_pages_start = 0
                remaining_pages_end = 0

            filename = f"{original_name}_{remaining_pages_start}-{remaining_pages_end}.pdf"
            output = os.path.join(output_folder, filename)
            with open(output, 'wb') as f:
                writer.write(f)
            print(f"Pages deleted, PDF saved as {filename}")

        elif num == 3:
            # Merge PDFs
            print("Enter the paths of PDFs to merge (comma-separated):")
            files_input = input("PDF paths: ").split(',')
            merger = PdfWriter()
            for file_path in files_input:
                file_path = file_path.strip()
                if os.path.exists(file_path):
                    merger.append(file_path)
                else:
                    print(f"File not found: {file_path}")
            output = os.path.join(output_folder, f"{original_name}_merged.pdf")
            merger.write(output)
            merger.close()
            print(f"PDFs merged and saved as {output}")

        elif num == 4:
            # Split PDF
            print("Enter the page range to split (e.g., 1-5):")
            pages_input = input("Pages to split: ")
            try:
                start, end = map(int, pages_input.split('-'))
                if start >= 1 and end <= total_pages and start <= end:
                    writer = PdfWriter()
                    for i in range(start - 1, end):
                        writer.add_page(pdf_reader.pages[i])
                    filename = f"{original_name}_{start}-{end}.pdf"
                    output = os.path.join(output_folder, filename)
                    with open(output, 'wb') as f:
                        writer.write(f)
                    print(f"PDF split saved as {filename}")
                else:
                    print("Invalid page range.")
            except ValueError:
                print("Invalid input format.")

        elif num == 5:
            # Rotate pages
            print("Enter the page numbers or ranges to rotate (e.g., 1,2,4-6):")
            pages_input = input("Pages to rotate: ")
            angle = int(input("Enter rotation angle (90, 180, 270): "))
            pages_to_rotate = set()

            for part in pages_input.split(','):
                if '-' in part:
                    start, end = part.split('-')
                    try:
                        start, end = int(start), int(end)
                        if start <= end and start >= 1:
                            pages_to_rotate.update(range(start - 1, end))  # Convert to 0-based index
                        else:
                            print(f"Invalid range: {part}")
                    except ValueError:
                        print(f"Invalid range format: {part}")
                else:
                    try:
                        page_number = int(part)
                        if page_number >= 1:
                            pages_to_rotate.add(page_number - 1)  # Convert to 0-based index
                        else:
                            print(f"Invalid page number: {part}")
                    except ValueError:
                        print(f"Invalid page number format: {part}")

            writer = PdfWriter()
            for i in range(total_pages):
                page = pdf_reader.pages[i]
                if i in pages_to_rotate:
                    page.rotate_clockwise(angle)
                writer.add_page(page)

            filename = f"{original_name}_rotated_{angle}.pdf"
            output = os.path.join(output_folder, filename)
            with open(output, 'wb') as f:
                writer.write(f)
            print(f"Pages rotated, PDF saved as {filename}")

        elif num == 6:
            # Add Watermark (Text)
            print("Enter the text to use as a watermark:")
            watermark_text = input("Watermark text: ")
            watermark_path = os.path.join(output_folder, "watermark.pdf")
            create_watermark_pdf(watermark_text, watermark_path)
            watermark_pdf = PdfReader(watermark_path)
            watermark_page = watermark_pdf.pages[0]
            writer = PdfWriter()
            for page in pdf_reader.pages:
                page.merge_page(watermark_page)
                writer.add_page(page)
            filename = f"{original_name}_watermarked.pdf"
            output = os.path.join(output_folder, filename)
            with open(output, 'wb') as f:
                writer.write(f)
            print(f"Watermarked PDF saved as {filename}")

        elif num == 7:
            # Extract Pages
            print("Enter the page numbers or ranges to extract (e.g., 1,2,4-6):")
            pages_input = input("Pages to extract: ")
            pages_to_extract = set()

            for part in pages_input.split(','):
                if '-' in part:
                    start, end = part.split('-')
                    try:
                        start, end = int(start), int(end)
                        if start <= end and start >= 1:
                            pages_to_extract.update(range(start - 1, end))  # Convert to 0-based index
                        else:
                            print(f"Invalid range: {part}")
                    except ValueError:
                        print(f"Invalid range format: {part}")
                else:
                    try:
                        page_number = int(part)
                        if page_number >= 1:
                            pages_to_extract.add(page_number - 1)  # Convert to 0-based index
                        else:
                            print(f"Invalid page number: {part}")
                    except ValueError:
                        print(f"Invalid page number format: {part}")

            if pages_to_extract:
                writer = PdfWriter()
                for page_index in sorted(pages_to_extract):
                    if 0 <= page_index < len(pdf_reader.pages):
                        writer.add_page(pdf_reader.pages[page_index])
                filename = f"{original_name}_extracted.pdf"
                output = os.path.join(output_folder, filename)
                with open(output, 'wb') as f:
                    writer.write(f)
                print(f"Pages extracted, PDF saved as {filename}")
            else:
                print("No pages selected for extraction.")
        else:
            print("Invalid option")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    print("Choose one of the following: ")
    print('''1. Delete Pages
2. Reverse PDF
3. Merge PDFs
4. Split PDF
5. Rotate Pages
6. Add Watermark (Text)
7. Extract Pages''')

    while True:
        try:
            num = int(input("Number = "))
            if 1 <= num <= 8:
                pdf_operation(num)
                break
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
