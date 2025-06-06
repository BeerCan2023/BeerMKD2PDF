import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                           QWidget, QFileDialog, QMessageBox, QLabel, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5 import QtGui
import markdown
import webbrowser
import tempfile
import pdfkit

class MarkdownToPDFConverter(QThread):
    progress = pyqtSignal(int)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)
    
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.is_file = os.path.isfile(path)
        
    def run(self):
        try:
            if self.is_file:
                self.convert_file(self.path)
            else:
                self.convert_directory(self.path)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def convert_file(self, file_path):
        if not file_path.lower().endswith('.md'):
            return
            
        output_path = os.path.splitext(file_path)[0] + '.pdf'
        self.convert_md_to_pdf(file_path, output_path)
        self.progress.emit(100)
    
    def convert_directory(self, directory):
        md_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.md'):
                    md_files.append(os.path.join(root, file))
        
        if not md_files:
            raise Exception("Aucun fichier Markdown (.md) trouvé dans le répertoire.")
        
        total_files = len(md_files)
        for i, file_path in enumerate(md_files, 1):
            output_path = os.path.splitext(file_path)[0] + '.pdf'
            self.convert_md_to_pdf(file_path, output_path)
            self.progress.emit(int((i / total_files) * 100))
    
    def convert_md_to_pdf(self, input_file, output_file):
        try:
            # Lire le contenu du fichier Markdown
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Convertir Markdown en HTML avec prise en charge des tableaux
            html = markdown.markdown(text, extensions=['tables'])
            
            # Créer un fichier HTML temporaire
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f:
                temp_html = f.name
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
                        h1, h2, h3 {{ color: #2c3e50; }}
                        code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
                        pre {{ background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                        blockquote {{ border-left: 4px solid #3498db; padding-left: 15px; color: #555; }}
                        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                        th {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                    {html}
                </body>
                </html>
                """)
            
            # Convertir HTML en PDF
            options = {
                'encoding': 'UTF-8',
                'quiet': ''
            }
            
            # Vérifier si wkhtmltopdf est dans le PATH
            try:
                config = pdfkit.configuration(wkhtmltopdf=pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_PATH', 'wkhtmltopdf')))
            except:
                config = None
            
            pdfkit.from_file(temp_html, output_file, configuration=config, options=options)
            
            # Supprimer le fichier temporaire
            os.unlink(temp_html)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la conversion de {input_file}: {str(e)}")

class MarkdownToPDFApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.converter = None
        
    def initUI(self):
        self.setWindowTitle('Markdown 2 PDF')
        self.setGeometry(100, 100, 500, 350)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel('Markdown 2 PDF')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; margin-bottom: 5px;')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Sous-titre
        subtitle_label = QLabel('by BeerCan.fr')
        subtitle_label.setStyleSheet('font-size: 14px; color: #666; margin-bottom: 20px;')
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        # Étiquette pour afficher le chemin sélectionné
        self.path_label = QLabel('Aucun fichier ou dossier sélectionné')
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet('margin: 10px 0;')
        layout.addWidget(self.path_label)
        
        # Bouton pour sélectionner un fichier
        self.select_file_btn = QPushButton('Sélectionner un fichier')
        self.select_file_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_btn)
        
        # Bouton pour sélectionner un dossier
        self.select_dir_btn = QPushButton('Sélectionner un dossier')
        self.select_dir_btn.clicked.connect(self.select_directory)
        layout.addWidget(self.select_dir_btn)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Étiquette de statut
        self.status_label = QLabel('Prêt')
        layout.addWidget(self.status_label)
        
        # Bouton de conversion
        self.convert_btn = QPushButton('Convertir en PDF')
        self.convert_btn.setEnabled(False)
        self.convert_btn.clicked.connect(self.start_conversion)
        layout.addWidget(self.convert_btn)
        
        # Ajouter un espacement
        layout.addStretch()
        
        # Logo et version
        logo_label = QLabel()
        logo_pixmap = QtGui.QPixmap('logo.png')
        # Redimensionner le logo à 50% de sa taille d'origine
        new_width = int(logo_pixmap.width() * 0.5)
        new_height = int(logo_pixmap.height() * 0.5)
        logo_pixmap = logo_pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet('margin: 20px 0 10px 0;')
        layout.addWidget(logo_label)
        
        # Version
        footer_label = QLabel('v1.1')
        footer_label.setStyleSheet('color: #888; font-size: 12px; margin-bottom: 10px;')
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)
        
        central_widget.setLayout(layout)
        
        # Variables
        self.selected_path = ''
        
    def select_file(self):
        # Ouvrir une boîte de dialogue pour sélectionner un fichier
        path, _ = QFileDialog.getOpenFileName(
            self, 
            'Sélectionner un fichier Markdown',
            '',
            'Fichiers Markdown (*.md);;Tous les fichiers (*)'
        )
        
        if path:
            self.selected_path = path
            self.path_label.setText(f'Fichier sélectionné: {path}')
            self.convert_btn.setEnabled(True)
            self.status_label.setText('Prêt à convertir')
            self.progress_bar.setValue(0)
    
    def select_directory(self):
        # Ouvrir une boîte de dialogue pour sélectionner un dossier
        path = QFileDialog.getExistingDirectory(
            self,
            'Sélectionner un dossier contenant des fichiers Markdown',
            '',
            QFileDialog.ShowDirsOnly
        )
        
        if path:
            self.selected_path = path
            self.path_label.setText(f'Dossier sélectionné: {path}')
            self.convert_btn.setEnabled(True)
            self.status_label.setText('Prêt à convertir')
            self.progress_bar.setValue(0)
    
    def start_conversion(self):
        if not self.selected_path:
            QMessageBox.warning(self, 'Erreur', 'Veuillez d\'abord sélectionner un fichier ou un dossier.')
            return
            
        self.status_label.setText('Conversion en cours...')
        self.select_file_btn.setEnabled(False)
        self.select_dir_btn.setEnabled(False)
        self.convert_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Démarrer le thread de conversion
        self.converter = MarkdownToPDFConverter(self.selected_path)
        self.converter.progress.connect(self.update_progress)
        self.converter.finished_signal.connect(self.conversion_finished)
        self.converter.error_signal.connect(self.conversion_error)
        self.converter.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def conversion_finished(self):
        self.status_label.setText('Conversion terminée avec succès!')
        self.select_file_btn.setEnabled(True)
        self.select_dir_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)
        QMessageBox.information(self, 'Succès', 'La conversion s\'est terminée avec succès!')
    
    def conversion_error(self, error_msg):
        self.status_label.setText('Erreur lors de la conversion')
        self.select_file_btn.setEnabled(True)
        self.select_dir_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)
        QMessageBox.critical(self, 'Erreur', f'Une erreur est survenue:\n{error_msg}')

def main():
    app = QApplication(sys.argv)
    
    # Vérifier si wkhtmltopdf est installé
    try:
        import pdfkit
        try:
            # Essayer de trouver wkhtmltopdf dans le PATH
            pdfkit.from_string('Test', 'test.pdf')
        except OSError:
            # Si non trouvé, demander à l'utilisateur de l'installer
            reply = QMessageBox.question(
                None,
                'wkhtmltopdf non trouvé',
                'Pour convertir les fichiers en PDF, vous devez installer wkhtmltopdf.\n\n' \
                'Souhaitez-vous ouvrir la page de téléchargement maintenant?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                webbrowser.open('https://wkhtmltopdf.org/downloads.html')
            
            return
    except ImportError:
        QMessageBox.critical(
            None,
            'Erreur',
            'Impossible d\'importer pdfkit. Veuillez l\'installer avec la commande suivante :\n\n' \
            'pip install pdfkit'
        )
        return
    
    # Vérifier si markdown est installé
    try:
        import markdown
    except ImportError:
        QMessageBox.critical(
            None,
            'Erreur',
            'Le module markdown n\'est pas installé. Veuillez l\'installer avec la commande suivante :\n\n' \
            'pip install markdown'
        )
        return
    
    # Démarrer l'application
    ex = MarkdownToPDFApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
