-- Define the roles available in the system
CREATE TYPE user_role AS ENUM ('ADMIN', 'TEACHER', 'STUDENT');

-- 1. Schools (The Top-Level Tenant)
CREATE TABLE schools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users (Handles Admins, Teachers, and Students)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Grades (e.g., 9th Grade, 10th Grade)
CREATE TABLE grades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    level_name VARCHAR(50) NOT NULL 
);

-- 4. Classes (The specific courses offered)
CREATE TABLE classes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grade_id UUID REFERENCES grades(id) ON DELETE CASCADE, -- ALTERED: Removed NOT NULL
    teacher_id UUID REFERENCES users(id), -- ALTERED: Removed NOT NULL so admins can assign later
    name VARCHAR(100) NOT NULL,
    description TEXT -- ALTERED: Added missing description column
);

-- 5. Enrollments (Junction table linking Students to Classes)
CREATE TABLE enrollments (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- ALTERED: Renamed from student_id to match Python router
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, class_id)
);

-- 6. Announcements (Updates, exam dates, etc.)
CREATE TABLE announcements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    class_id UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    author_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Attachments (Links to cloud storage files)
CREATE TABLE attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    announcement_id UUID NOT NULL REFERENCES announcements(id) ON DELETE CASCADE,
    file_url TEXT NOT NULL,
    file_type VARCHAR(50) NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);