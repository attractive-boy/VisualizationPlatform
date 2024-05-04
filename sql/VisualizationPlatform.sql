--CREATE UNIQUE INDEX idx_year_province_city ON scorestatistics_scorestatistics (year, province, city);

DELIMITER //

-- 创建插入触发器
CREATE TRIGGER after_insert_score
AFTER INSERT ON scores_score
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(8,2);
    DECLARE @new_liberal_arts_count INT;
    DECLARE @new_science_count INT;

    -- 计算总分
    SET total = NEW.biology + NEW.chemistry + NEW.english + NEW.geography + NEW.history + NEW.language + NEW.mathematics + NEW.physics + NEW.politics;

    -- 计算文理科生数量
    IF NEW.history + NEW.politics + NEW.geography > 0 THEN
        SET @new_liberal_arts_count = 1;
    ELSE
        SET @new_liberal_arts_count = 0;
    END IF;

    IF NEW.biology + NEW.chemistry + NEW.physics > 0 THEN
        SET @new_science_count = 1;
    ELSE
        SET @new_science_count = 0;
    END IF;

    -- 插入统计表中的数据
    INSERT INTO scorestatistics_scorestatistics (year, province, city, data_count, total_score, pass_count, language_score, mathematics_score, english_score, chemistry_score, physics_score, biology_score, geography_score, politics_score, history_score, liberal_arts_count, science_count)
    VALUES (NEW.year, NEW.province, NEW.city, 1 , total, NEW.score >= @PASS_SCOPE, NEW.language, NEW.mathematics, NEW.english, NEW.chemistry, NEW.physics, NEW.biology, NEW.geography, NEW.politics, NEW.history, @new_liberal_arts_count, @new_science_count)
    ON DUPLICATE KEY UPDATE
    data_count = data_count + 1,
    total_score = total_score + total,
    pass_count = pass_count + (NEW.score >= @PASS_SCOPE),
    language_score = language_score + NEW.language,
    mathematics_score = mathematics_score + NEW.mathematics,
    english_score = english_score + NEW.english,
    chemistry_score = chemistry_score + NEW.chemistry,
    physics_score = physics_score + NEW.physics,
    biology_score = biology_score + NEW.biology,
    geography_score = geography_score + NEW.geography,
    politics_score = politics_score + NEW.politics,
    history_score = history_score + NEW.history,
    liberal_arts_count = liberal_arts_count + @new_liberal_arts_count,
    science_count = science_count + @new_science_count;
END;
//

-- 创建更新触发器
CREATE TRIGGER after_update_score
AFTER UPDATE ON scores_score
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(8,2);
    DECLARE @new_liberal_arts_count INT;
    DECLARE @new_science_count INT;

    -- 计算总分
    SET total = NEW.biology + NEW.chemistry + NEW.english + NEW.geography + NEW.history + NEW.language + NEW.mathematics + NEW.physics + NEW.politics;

    -- 计算文理科生数量
    IF NEW.history + NEW.politics + NEW.geography > 0 THEN
        SET @new_liberal_arts_count = 1;
    ELSE
        SET @new_liberal_arts_count = 0;
    END IF;

    IF NEW.biology + NEW.chemistry + NEW.physics > 0 THEN
        SET @new_science_count = 1;
    ELSE
        SET @new_science_count = 0;
    END IF;

    -- 更新统计表中的数据
    UPDATE scorestatistics_scorestatistics
    SET total_score = total_score + total - OLD.biology - OLD.chemistry - OLD.english - OLD.geography - OLD.history - OLD.language - OLD.mathematics - OLD.physics - OLD.politics,
        pass_count = pass_count + (NEW.score >= @PASS_SCOPE) - (OLD.score >= @PASS_SCOPE),
        language_score = language_score + NEW.language - OLD.language,
        mathematics_score = mathematics_score + NEW.mathematics - OLD.mathematics,
        english_score = english_score + NEW.english - OLD.english,
        chemistry_score = chemistry_score + NEW.chemistry - OLD.chemistry,
        physics_score = physics_score + NEW.physics - OLD.physics,
        biology_score = biology_score + NEW.biology - OLD.biology,
        geography_score = geography_score + NEW.geography - OLD.geography,
        politics_score = politics_score + NEW.politics - OLD.politics,
        history_score = history_score + NEW.history - OLD.history,
        liberal_arts_count = liberal_arts_count + @new_liberal_arts_count - OLD.liberal_arts_count,
        science_count = science_count + @new_science_count - OLD.science_count
    WHERE year = NEW.year AND province = NEW.province AND city = NEW.city;
END;
//

-- 创建删除触发器
CREATE TRIGGER after_delete_score
AFTER DELETE ON scores_score
FOR EACH ROW
BEGIN
    DECLARE total DECIMAL(8,2);
    DECLARE @new_liberal_arts_count INT;
    DECLARE @new_science_count INT;

    -- 计算总分
    SET total = OLD.biology + OLD.chemistry + OLD.english + OLD.geography + OLD.history + OLD.language + OLD.mathematics + OLD.physics + OLD.politics;

    -- 计算文理科生数量
    IF OLD.history + OLD.politics + OLD.geography > 0 THEN
        SET @new_liberal_arts_count = 1;
    ELSE
        SET @new_liberal_arts_count = 0;
    END IF;

    IF OLD.biology + OLD.chemistry + OLD.physics > 0 THEN
        SET @new_science_count = 1;
    ELSE
        SET @new_science_count = 0;
    END IF;

    -- 更新统计表中的数据
    UPDATE scorestatistics_scorestatistics
    SET data_count = data_count - 1,
        total_score = total_score - OLD.biology - OLD.chemistry - OLD.english - OLD.geography - OLD.history - OLD.language - OLD.mathematics - OLD.physics - OLD.politics,
        pass_count = pass_count - (OLD.score >= @PASS_SCOPE),
        language_score = language_score - OLD.language,
        mathematics_score = mathematics_score - OLD.mathematics,
        english_score = english_score - OLD.english,
        chemistry_score = chemistry_score - OLD.chemistry,
        physics_score = physics_score - OLD.physics,
        biology_score = biology_score - OLD.biology,
        geography_score = geography_score - OLD.geography,
        politics_score = politics_score - OLD.politics,
        history_score = history_score - OLD.history,
        liberal_arts_count = liberal_arts_count - @new_liberal_arts_count,
        science_count = science_count - @new_science_count
    WHERE year = OLD.year AND province = OLD.province AND city = OLD.city;
END;
//

DELIMITER ;
