from django.contrib import admin
from .models import Forum, Profile, Comment, VotingOption, News, Docs


class VotinsInline(admin.TabularInline):
    model = VotingOption
    extra = 1
    # fk_name = 'Forum'

class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    # list_display = ['title', 'author', 'get_voters']
    inlines = [
        VotinsInline,
        CommentInline,
    ]
    # def get_voters(self, obj):
    #     voters = obj.voters.all()
    #     return ", ".join([voter.username for voter in voters])

    # get_voters.short_description = 'Проголосовавшие'

@admin.register(Profile)
class ProfiileAdmin(admin.ModelAdmin):
    pass

admin.site.register(News)
admin.site.register(Docs)

# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     pass

# class VotingAdmin(admin.ModelAdmin):
#     pass

# class VotingOptionAdmin(admin.ModelAdmin):
#     pass

@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'forum', 'get_voters')
    def get_voters(self, obj):
        voters = obj.voters.all()
        return ", ".join([voter.username for voter in voters])

    get_voters.short_description = 'Проголосовавшие'

# admin.site.register(Profile, ProfiileAdmin)
# admin.site.register(Forum, ForumAdmin)
# admin.site.register(Voting, VotingAdmin)
# admin.site.register(VotingOption, VotingOptionAdmin)
