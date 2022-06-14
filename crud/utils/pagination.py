from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11):

        self.base_url = base_url
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                raise Exception()
        except Exception as e:
            self.current_page = 1
        self.query_params = query_params
        self.per_page = per_page
        self.all_count = all_count
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):

        return (self.current_page - 1) * self.per_page

    @property
    def end(self):

        return self.current_page * self.per_page

    def page_html(self):

        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:

            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:

                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_end = self.pager_count
                    pager_start = self.pager_count - self.pager_page_count + 1
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []

        if self.current_page <= 1:
            prev = '<li><a href="#">Next</a></li>'
        else:
            self.query_params['page'] = self.current_page - 1
            prev = '<li><a href="%s?%s">Prev</a></li>' % (self.base_url, self.query_params.urlencode())
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="active"><a href="%s?%s">%s</a></li>' % (
                    self.base_url, self.query_params.urlencode(), i,)
            else:
                tpl = '<li><a href="%s?%s">%s</a></li>' % (self.base_url, self.query_params.urlencode(), i,)
            page_list.append(tpl)

        if self.current_page >= self.pager_count:
            nex = '<li><a href="#">Next</a></li>'
        else:
            self.query_params['page'] = self.current_page + 1
            nex = '<li><a href="%s?%s">Next</a></li>' % (self.base_url, self.query_params.urlencode(),)
        page_list.append(nex)
        page_str = "".join(page_list)
        return mark_safe(page_str)
