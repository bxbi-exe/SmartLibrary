package mk.ukim.finki.smartlibrary.DTOs;

import java.io.File;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UploadDocumentDTO {
  private Long categoryId;
  private File file;
  private Long userId;
  private String description;

}