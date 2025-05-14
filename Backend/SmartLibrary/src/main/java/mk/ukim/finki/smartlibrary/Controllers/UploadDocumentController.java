package mk.ukim.finki.smartlibrary.Controllers;

import mk.ukim.finki.smartlibrary.Models.UploadDocument;
import mk.ukim.finki.smartlibrary.Service.UploadDocumentService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import mk.ukim.finki.smartlibrary.DTOs.UploadDocumentDTO;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/upload-documents")
public class UploadDocumentController {

    private final UploadDocumentService uploadDocumentService;

    public UploadDocumentController(UploadDocumentService uploadDocumentService) {
        this.uploadDocumentService = uploadDocumentService;
    }

    @GetMapping
    public List<UploadDocument> getAllUploadDocuments() {
        return uploadDocumentService.findAll();
    }

    @GetMapping("/{id}")
    public Optional<UploadDocument> getUploadDocumentById(@PathVariable Long id) {
        return uploadDocumentService.findById(id);
    }

    @GetMapping("/user/{userId}")
    public List<UploadDocument> getUploadDocumentsByUserId(@PathVariable Long userId) {
        return uploadDocumentService.findByUserId(userId);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UploadDocument createUploadDocument(@RequestBody UploadDocument uploadDocument) {
        return uploadDocumentService.create(uploadDocument);
    }

    @PutMapping("/{id}")
    public Optional<UploadDocument> updateUploadDocument(@PathVariable Long id, @RequestBody UploadDocument uploadDocument) {
        return uploadDocumentService.update(id, uploadDocument);
    }

    @DeleteMapping("/{id}")
    public boolean deleteUploadDocument(@PathVariable Long id) {
        return uploadDocumentService.delete(id);
    }

    @PostMapping("/upload")
    @ResponseStatus(HttpStatus.CREATED)
    public Long uploadDocument(@RequestBody UploadDocumentDTO uploadDocument) {
        return uploadDocumentService.upload(uploadDocument);
    }
}
