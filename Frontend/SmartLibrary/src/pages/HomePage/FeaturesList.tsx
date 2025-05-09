import React from "react";
import styles from "./home.module.css";

const FeaturesList: React.FC = () => {
  return (
    <section className={styles.features}>
      <h2>👩‍🏫 Карактеристики:</h2>
      <ul>
        <li>🚀 Автоматско генерирање на тестови и Q&A</li>
        <li>🚀 Поддршка за повеќе формати (PDF, DOCX, CSV, TXT)</li>
        <li>🚀 Категоризација, филтрирање и пребарување</li>
        <li>🚀 Интуитивен и модерен интерфејс</li>
        <li>🚀 100% компатибилно со мобилни уреди</li>
      </ul>
    </section>
  );
};

export default FeaturesList;
