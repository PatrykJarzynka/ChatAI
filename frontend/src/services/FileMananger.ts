import { Injectable, signal } from '@angular/core';
import { StatusType } from '@enums/StatusType';
import { FileUploader } from '@services/FileUploader';
import { UploadedFile } from '@appTypes/UploadedFile';
import { FileValidator } from '@services/FileValidator';


@Injectable({
  providedIn: 'root',
})
export class FileManager {

  private files = signal<UploadedFile[]>([]);
  private selectedFilesIds = signal<Set<number>>(new Set());

  constructor(private fileUploader: FileUploader, private fileValidator: FileValidator) {
  }

  getFiles() {
    return this.files;
  }

  getSelectedFilesIds() {
    return this.selectedFilesIds;
  }

  insertFileTemplate(file: File): void {
    this.files.update(files => {
      files.push({
        id: files.length,
        name: file.name,
        status: StatusType.Pending
      });

      return files;
    });
  }

  updateFileAfterUpload(fileId: number | null, status: StatusType, temporaryFileId: number): void {
    this.files.update(files =>
      files.map(file => file.id === temporaryFileId
        ? { ...file, status: status, id: fileId ?? file.id }
        : file)
    );
  }

  updateSelectedFiles(selectedFileId: number): void {
    this.selectedFilesIds.update(currentIds => {
      if (currentIds.has(selectedFileId)) {
        currentIds.delete(selectedFileId);
      } else {
        currentIds.add(selectedFileId);
      }

      return currentIds;
    });
  }

  async onFilesUpload(files: File[]): Promise<void> {
    for (const file of files) {
      const isFileValid = this.fileValidator.validateFile(file);

      if (!isFileValid) {
        return;
      }

      const temporaryFileID = this.files().length;

      this.insertFileTemplate(file);

      try {
        const response = await this.fileUploader.upload(file);
        this.updateFileAfterUpload(response.fileId, StatusType.Success, temporaryFileID);
      } catch {
        this.updateFileAfterUpload(null, StatusType.Failed, temporaryFileID);
      }

    }
  }
}
