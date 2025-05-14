import React, { useEffect, useState } from 'react';

const UploadCard = () => {
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [description, setDescription] = useState('');
    const [file, setFile] = useState(null);

    const user = JSON.parse(localStorage.getItem('user'));
    const userId = user?.id;

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await fetch('http://localhost:8080/api/categories');
                if (!response.ok) throw new Error('Failed to fetch categories');
                const data = await response.json();
                console.log(data)
                setCategories(data);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };

        fetchCategories();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file || !selectedCategory || !description) {
            alert("Сите полиња се задолжителни!");
            return;
        }

        const formData = new FormData();
        formData.append("categoryId", selectedCategory);
        formData.append("file", file);
        formData.append("userId", userId);
        formData.append("description", description);

        try {
            const response = await fetch("http://localhost:8080/api/upload-documents/upload", {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                alert("Фајлот е успешно прикачен!");
                setFile(null);
                setDescription('');
                setSelectedCategory('');
            } else {
                const errorData = await response.json();
                alert(`Грешка при прикачување: ${errorData.message || 'Непозната грешка'}`);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("Настана грешка при поврзување со серверот.");
        }
    };

    return (
        <>
            <style>{`
                .upload-card {
                    background: white;
                    padding: 30px;
                    border-radius: 15px;
                    width: 400px;
                    box-shadow: 0 0 15px rgba(0,0,0,0.05);
                    position: relative;
                    left: 200px;
                    top: 30px;
                }
                .upload-card h3 {
                    text-align: center;
                    color: #1f74d1;
                    margin-bottom: 20px;
                }
                .upload-card label {
                    display: block;
                    margin-top: 15px;
                }
                .upload-card select,
                .upload-card input[type="file"],
                .upload-card textarea {
                    margin-top: 10px;
                    width: 100%;
                    padding: 6px;
                    box-sizing: border-box;
                }
                .upload-card textarea {
                    resize: vertical;
                    min-height: 80px;
                    max-height: 150px;
                }
                .upload-btn {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    margin-top: 20px;
                    border-radius: 6px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 5px;
                    justify-content: center;
                }
                .upload-btn:hover {
                    background-color: #1e40af;
                }
            `}</style>

            <div className="upload-card">
                <h3>Изберете образовен материјал за прикачување</h3>
                <form onSubmit={handleSubmit}>
                    <input type="file" onChange={(e) => setFile(e.target.files[0])} />

                    <label htmlFor="category">Категорија:</label>
                    <select
                        id="category"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="" disabled>-- Избери категорија --</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </select>

                    <label htmlFor="description">Опис:</label>
                    <textarea
                        id="description"
                        maxLength={200}
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Напишете краток опис..."
                    ></textarea>

                    <button type="submit" className="upload-btn">
                        📤 Прикачи
                    </button>
                </form>
            </div>
        </>
    );
};

export default UploadCard;
