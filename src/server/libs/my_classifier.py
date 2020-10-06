""" my_classifier.py: class that creates automatic comments over
user's performance on a given composition.
"""


class MyClassifier(object):
    """ Creates automatic comments over user's performance on a given
    composition.

    The TextCommenter class is responsible to evaluate which patterns
    of the model letrus.models.AutomaticTextComment applies to the given
    given composition.

    If more than one comment matches the given pattern, the comments will be
    sorted by their priority field.

    Example:
        from compositions.models import Composition
        from letrus.autocomment import TextCommenter

        composition = Composition.objects.get(id=3)
        commenter = TextCommenter(composition)
        print commenter.make_comments()

    In order to parse special tags on the comments, you should use the class
    letrus.autocomment.LetrusCommentParser on the resulting comments.

    Example:
        parser = LetrusCommentParser(composition=composition)
        for c in commenter.make_comments():
            print parser.parse(c['comment'])
    """

    CACHE_VARNAME = "text_comments_cache"
    CACHE_ENABLED = True
    text_rules = None

    def __init__(self, composition:dict , genre:dict , text_rules:list):

        self.composition = composition
        self.text_rules = text_rules
        self.genre = genre

    async def make_comments_for_report(self, parser=None):
        """Filter comments by type (positive, negative and neutral).
        """
        return self.filtered_comments_by_type(await self.make_comments(parser=parser))

    async def make_comments(self, parser=None):
        """ Make all text comments about the given composition.

        Text comments are also known as general comments and are usually
        presented to students right after they finish a composition. These
        comments are also used in the "auto correction" feature on the
        reviewers' page, sending the comments to the general comments section,
        where the reviewer is free to adapt them.

        Returns:
            dict: a list of dictionaries in the following form, representing a
                letrus.models.AutomaticTextComment model:

                {
                    "rule": int,
                    "comment": str,
                    "priority": int,
                    "n_items": int,
                }
        """
        # if self.CACHE_ENABLED:
        #     comments = self._restore_cache()

        #     if comments is not None:
        #         return comments

        comments = []
         # TODO - MAKE A SEARCH HERE INSTEAD OF MANUAL ORDERING
        ordered_rules = sorted(self.text_rules, key=lambda x: x["priority"], reverse = True)
        varnames = set()
        for rule in ordered_rules:
            for item in rule['items']:
                varnames.add(item["type"]["varname"])
        paragraphs = get_paragraphs(self.composition["composition_raw"])
        marker_map = {}

        for varname in varnames:
            if not marker_map.get(varname):
                marker_map[varname] = process_paragraphs_with_markers(
                    paragraphs, [varname], ordered_rules
                )
        for rule in ordered_rules:
            if self._rule_matches(rule, marker_map, paragraphs):
                _comment = rule["comment"]
                if parser:
                    _comment = await parser.parse(_comment)

                comments.append(
                    {
                        "rule": rule["id"],
                        "comment": _comment,
                        "priority": rule["priority"],
                        "type": rule["type"],
                        "n_items": len(rule["items"]),
                    }
                )

        comments_sorted = sorted(
            comments, key=itemgetter("priority"), reverse=True
        )

        return comments_sorted

    @staticmethod
    def filtered_comments_by_type(comments):
        """ Filter comments by type (positive, negative and neutral).
        """
        flag_positive, flag_negative, flag_neutral = False, False, 0
        filtered_comments = []

        for comment in comments:
            if comment["type"] == "positive" and not flag_positive:
                filtered_comments.append((comment, 1))
                flag_positive = True
            if comment["type"] == "negative" and not flag_negative:
                filtered_comments.append((comment, 2))
                flag_negative = True
            if comment["type"] == "neutral" and flag_neutral < 2:
                filtered_comments.append((comment, 3))
                flag_neutral += 1

        # Sort comments by type
        filtered_comments.sort(key=lambda tup: tup[1])

        return [it[0] for it in filtered_comments]

    def get_restrict_set(self, restrict_set):
        """ Get restrict set.
        """
        if restrict_set is not None and restrict_set != "":
            return [w.strip() for w in restrict_set.split(",")]
        return None

    def _rule_matches(self, rule, marker_map, paragraphs):
        for item in rule['items']:
            markers = marker_map[item['type']['varname']]
            matches = get_occurrences(
                markers,
                n_paragraphs=len(paragraphs),
                section=item["text_section"],
                unique=item["unique"],
                subset= self.get_restrict_set(item["restrict_set"]),
            )

            nitems = len(matches)
            try:
                if item["comparator"] == "==" and nitems != int(item["range"]):
                    return False
                if item["comparator"] == ">=" and nitems < int(item["range"]):
                    return False
                if item["comparator"] == "<=" and nitems > int(item["range"]):
                    return False
                if item["comparator"] == "in":
                    first, last = item["range"].split("-")
                    if nitems < int(first) or nitems > int(last):
                        return False
                if item["comparator"] == ">#":

                    over_limit_matches = get_occurrences_count(
                        markers,
                        min_threshold=int(item["range"]) + 1,
                        section=item["text_section"],
                        unique=item["unique"],
                        subset=get_restrict_set(item["restrict_set"]),
                    )

                    if not over_limit_matches:
                        return False

            except ValueError as e:
                logging.error(
                    "Ignoring AutomaticTextComment #%d, item #%d.",
                    rule["id"],
                    item["id"],
                )
                logging.error(e)

                return False

        return True


    # def _restore_cache(self):
    #     try:
    #         json_cache = CompositionJSONMetadata.objects.get(
    #             composition=self.composition, name=self.CACHE_VARNAME
    #         )

    #         cache_obj = json.loads(json_cache.value)

    #         # Verifying if cache is still hot
    #         composition_unchanged = True
    #         rule_unchanged = True

    #         # Check if composition has changed
    #         if cache_obj["hash"] != self.composition.cache_key():
    #             composition_unchanged = False

    #         # Check if rule has changed
    #         if AutomaticTextComment.objects.filter(
    #             modified__gt=json_cache.modified
    #         ).exists():
    #             rule_unchanged = False

    #         # Check if rule item has changed
    #         if AutomaticTextCommentItem.objects.filter(
    #             modified__gt=json_cache.modified
    #         ).exists():
    #             rule_unchanged = False

    #         if composition_unchanged and rule_unchanged:
    #             LOGGER.info(
    #                 "Cache hit: %s (composition=%d)",
    #                 self.CACHE_VARNAME,
    #                 self.composition.id,
    #             )
    #             # Add comment type (positive, negativem neutral)
    #             try:
    #                 comments = cache_obj["comments"]
    #                 for comment in comments:
    #                     rule = AutomaticTextComment.objects.get(
    #                         id=comment["rule"]
    #                     )
    #                     comment["type"] = rule.type
    #                 return comments
    #             # pylint: disable=bare-except
    #             except:
    #                 json_cache.delete()  # Invalidates cache
    #         else:
    #             json_cache.delete()  # Invalidates cache
    #     except CompositionJSONMetadata.DoesNotExist:
    #         pass

    #     return None
