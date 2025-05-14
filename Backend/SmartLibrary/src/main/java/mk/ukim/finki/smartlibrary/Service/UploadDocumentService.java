package mk.ukim.finki.smartlibrary.Service;

import mk.ukim.finki.smartlibrary.DTOs.UploadDocumentDTO;
import mk.ukim.finki.smartlibrary.Enums.FileType;
import mk.ukim.finki.smartlibrary.Models.Category;
import mk.ukim.finki.smartlibrary.Models.UploadDocument;
import mk.ukim.finki.smartlibrary.Models.User;
import mk.ukim.finki.smartlibrary.Repository.UploadDocumentRepository;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class UploadDocumentService {

    private final UploadDocumentRepository repo;
    private final UserService userService;
    private final CategoryService categoryService;

    public UploadDocumentService(UploadDocumentRepository repo, UserService userService, CategoryService categoryService) {
        this.categoryService = categoryService;
        this.userService = userService;
        this.repo = repo;
    }

    public List<UploadDocument> findAll() {
        return repo.findAll();
    }

    public Optional<UploadDocument> findById(Long id) {
        return repo.findById(id);
    }

    public List<UploadDocument> findByUserId(Long userId) {
        return repo.findByUserId(userId);
    }

    public UploadDocument create(UploadDocument doc) {
        return repo.save(doc);
    }


    public Optional<UploadDocument> update(Long id, UploadDocument in) {
        return repo.findById(id).map(existing -> {
            existing.setFileName(in.getFileName());
            existing.setDescription(in.getDescription());
            existing.setFileType(in.getFileType());
            existing.setProcessed(in.isProcessed());
            existing.setUploadedDate(in.getUploadedDate());
            existing.setUser(in.getUser());
            existing.setCategories(in.getCategories());
            return repo.save(existing);
        });
    }

    public boolean delete(Long id) {
        if (!repo.existsById(id)) return false;
        repo.deleteById(id);
        return true;
    }

    public Long upload(UploadDocumentDTO uploadDocumentDTO) {
        User user = userService.findById(uploadDocumentDTO.getUserId())
                .orElseThrow(() -> new RuntimeException("User not found"));

        Category category = categoryService.findById(uploadDocumentDTO.getCategoryId())
                .orElseThrow(() -> new RuntimeException("Category not found"));

        List<Category> categories = new ArrayList<>();
        categories.add(category);

        FileType fileType = FileType.fromFileName(uploadDocumentDTO.getFile().getName());
                
        UploadDocument uploadDocument = new UploadDocument();
        uploadDocument.setFileName(uploadDocumentDTO.getFile().getName());
        uploadDocument.setDescription(uploadDocumentDTO.getDescription());
        uploadDocument.setProcessed(false);
        uploadDocument.setUploadedDate(new java.util.Date());
        uploadDocument.setUser(user);
        uploadDocument.setCategories(categories);
        uploadDocument.setFile(uploadDocumentDTO.getFile());
        uploadDocument.setFileType(fileType);
        return repo.save(uploadDocument).getId();
    }
}
