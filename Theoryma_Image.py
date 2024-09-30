import fitz
import os
from PIL import Image
from pdf2image import convert_from_path

def menu():
    print("\033[91m")
    print(
    """
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * *                                                                                          
    *                                                                                           *
    *  MMP""MM""YMM `7MM                                                                        *
    *  P'   MM   `7   MM                                                                        * 
    *       MM        MMpMMMb.  .gP"Ya   ,pW"Wq.`7Mb,od8 `7M'   `MF'`7MMpMMMb.pMMMb.   ,6"Yb.   *
    *       MM        MM    MM ,M'   Yb 6W'   `Wb MM' "'   VA   ,V    MM    MM    MM  8)   MM   * 
    *       MM        MM    MM 8M====== 8M     M8 MM        VA ,V     MM    MM    MM   ,pm9MM   *
    *       MM        MM    MM YM.    , YA.   ,A9 MM         VVV      MM    MM    MM  8M   MM   *
    *     .JMML.    .JMML  JMML.`Mbmmd'  `Ybmd9'.JMML.       ,V     .JMML  JMML  JMML.`Moo9^Yo. *
    *                                                      ,V                                   *
    *                                                    OOb"                                   *
    * Theoryma Image 1.0                                                                        *
    * Coded by Febrian Dani Ritonga                                                             *
    *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * * 
    """)
    print("\033[0m")
    print('==============================================')
    print('-----------MENU - Theoryma Image 1.0----------')
    print('==============================================')
    print('1. Convert PDF to Images')
    print('2. Convert Images to PDF')
    print('3. Merge Two PDFs')
    print('99. Donate Developer')
    print('0. Exit')
  
def pdf_to_images(input_file, output_folder):
    # Buka file PDF
    doc = fitz.open(input_file)

    # Ambil nama file PDF tanpa ekstensi
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    image_files = []  # List untuk menyimpan nama file yang dihasilkan
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap()

        # Buat nama file gambar dengan format base_name_theoryma-image + index + .png
        image_name = f"{base_name}_theoryma-image{i + 1}.png"
        image_path = os.path.join(output_folder, image_name)

        # Simpan gambar
        pix.save(image_path)

        # Tambahkan nama file ke list
        image_files.append(image_name)

    doc.close()  # Tutup dokumen PDF
    
    return image_files, base_name 

def images_to_pdf(image_files, output_pdf):
    images = []
    for image_file in image_files:
        img = Image.open(image_file)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        images.append(img)

    images[0].save(output_pdf, save_all=True, append_images=images[1:])
    return output_pdf

def merge_pdfs(pdf1, pdf2, output_pdf):
    doc1 = fitz.open(pdf1)
    doc2 = fitz.open(pdf2)

    doc1.insert_pdf(doc2)
    doc1.save(output_pdf)

    doc1.close()
    doc2.close()

    return output_pdf

def donate():
    print("""
          BTC     : 1FiCGtqBxCa7f2inWpYQNS44FnNEXrWsyF
          
          Thanks for your support 🙏
          """)

import os

def sanitize_path(path):
    """Menghilangkan tanda kutip ganda atau tunggal dari awal dan akhir path jika ada."""
    path = path.strip()  # Menghilangkan spasi ekstra
    if (path.startswith('"') and path.endswith('"')) or (path.startswith("'") and path.endswith("'")):
        # Jika ada tanda kutip yang berpasangan di awal dan akhir, hilangkan keduanya
        path = path[1:-1]
    elif path.startswith('"') or path.startswith("'"):
        # Jika hanya ada tanda kutip di awal, hilangkan tanda kutip di awal
        path = path[1:]
    elif path.endswith('"') or path.endswith("'"):
        # Jika hanya ada tanda kutip di akhir, hilangkan tanda kutip di akhir
        path = path[:-1]
    return path


def start():
    while True:
        menu()
        choice = input("Choose an option: ")
        
        if choice == '1':
            input_file = sanitize_path(input(f"Enter the path to the PDF file (e.i C:/Folder/file.pdf): "))
            output_folder = sanitize_path(input(f"Enter the output folder path (e.i C:/Folder/): "))
            
            # Proses PDF ke gambar
            image_files, base_name = pdf_to_images(input_file, output_folder)
            print("\033[92mPDF has been converted to images successfully.\033[0m")
            for i in range(len(image_files)):
                print(f"\033[92m{base_name}_theoryma-image{i + 1}.png\033[0")
        elif choice == '2':
            image_files = sanitize_path(input(f"Enter the paths to the image files, separated by commas (e.g., C:/Folder/image1.jpg, next file): ")).split(',')
            output_pdf = sanitize_path(input(f"Enter the path to the output PDF file (e.g., C:/Folder/output.pdf): "))
            result_pdf = images_to_pdf(image_files, output_pdf)
            print(f"\033[92mImages have been converted to PDF successfully: {result_pdf}\033[0m")

        elif choice == '3':
            pdf1 = sanitize_path(input(f"Enter the path to the first PDF file (e.g., C:/Folder/file1.pdf): "))
            pdf2 = sanitize_path(input(f"Enter the path to the second PDF file (e.g., C:/Folder/file2.pdf): "))
            output_pdf = sanitize_path(input("Enter the path to the output PDF file (e.g., C:/Folder/output.pdf): "))
            result_pdf = merge_pdfs(pdf1, pdf2, output_pdf)
            print(f"\033[92mPDFs have been merged successfully: {result_pdf}\033[0m")

        elif choice == '99':
            donate()
        elif choice == '0':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice. Please try again.")