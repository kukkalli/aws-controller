
# Minimal scaffolding for network-independent resources (extend per your needs).

resource "aws_ecr_repository" "app" {
  name                 = "${var.project_name}"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration { scan_on_push = true }
  tags = { Project = var.project_name }
}

output "ecr_repo_url" {
  value = aws_ecr_repository.app.repository_url
}
