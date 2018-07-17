# Generated by Django 2.0.5 on 2018-06-26 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20180616_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trouble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='内容')),
                ('ctime', models.DateTimeField(verbose_name='创建时间')),
                ('status', models.IntegerField(choices=[(1, '未处理'), (2, '处理中'), (3, '已处理')], default=1)),
                ('solution', models.TextField(null=True)),
                ('ptime', models.DateTimeField(null=True)),
                ('pj', models.IntegerField(choices=[(1, '不满意'), (2, '一般'), (3, '很好')], default=1, null=True)),
                ('processer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p', to='repository.UserInfo', verbose_name='处理者')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u', to='repository.UserInfo', verbose_name='提交人')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='article_type_id',
            field=models.IntegerField(choices=[(1, 'python'), (2, 'linux'), (3, 'java'), (4, 'go'), (5, 'openstack')], default=None, verbose_name='系统定义）'),
        ),
        migrations.AlterField(
            model_name='articledetail',
            name='article',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='detail', to='repository.Article', verbose_name='所属文章'),
        ),
    ]